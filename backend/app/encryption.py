import base64
from typing import ByteString


SECRET_KEY = "my_secret_key_123"
SHIFT_VALUE = 3


def _xor_bytes(data: bytes, key: str = SECRET_KEY) -> bytes:
    """
    XOR each byte with repeating key bytes.
    XOR is reversible:
    data XOR key XOR key = data
    """
    key_bytes = key.encode("utf-8")
    return bytes(
        byte ^ key_bytes[i % len(key_bytes)]
        for i, byte in enumerate(data)
    )


def _shift_bytes(data: bytes, shift: int = SHIFT_VALUE) -> bytes:
    """
    Shift each byte forward.
    We use modulo 256 because byte values must stay between 0 and 255.
    """
    return bytes((byte + shift) % 256 for byte in data)


def _unshift_bytes(data: bytes, shift: int = SHIFT_VALUE) -> bytes:
    """
    Reverse byte shifting.
    """
    return bytes((byte - shift) % 256 for byte in data)


def _scramble_bytes(data: bytes) -> bytes:
    """
    Simple reversible scrambling:
    split bytes into even-indexed and odd-indexed positions.
    
    Example:
    original indexes: 0 1 2 3 4 5
    scrambled:        0 2 4 1 3 5
    """
    even_bytes = data[::2]
    odd_bytes = data[1::2]
    return even_bytes + odd_bytes


def _unscramble_bytes(data: bytes) -> bytes:
    """
    Reverse of _scramble_bytes().
    """
    length = len(data)
    even_length = (length + 1) // 2

    even_bytes = data[:even_length]
    odd_bytes = data[even_length:]

    result = bytearray(length)

    result[::2] = even_bytes
    result[1::2] = odd_bytes

    return bytes(result)


def encrypt_bytes(data: ByteString) -> str:
    """
    Encrypt any bytes data and return Base64 string.
    Works for text bytes and image bytes.
    """
    if not data:
        raise ValueError("Input data cannot be empty.")

    data = bytes(data)

    step_1 = _xor_bytes(data)
    step_2 = _shift_bytes(step_1)
    step_3 = _scramble_bytes(step_2)
    encrypted = base64.b64encode(step_3).decode("utf-8")

    return encrypted


def decrypt_bytes(encrypted_data: str) -> bytes:
    """
    Decrypt Base64 encrypted string back to original bytes.
    """
    if not encrypted_data:
        raise ValueError("Encrypted data cannot be empty.")

    step_1 = base64.b64decode(encrypted_data.encode("utf-8"))
    step_2 = _unscramble_bytes(step_1)
    step_3 = _unshift_bytes(step_2)
    decrypted = _xor_bytes(step_3)

    return decrypted


def encrypt_text(text: str) -> str:
    """
    Encrypt normal text.
    """
    if not text:
        raise ValueError("Text cannot be empty.")

    return encrypt_bytes(text.encode("utf-8"))


def decrypt_text(encrypted_text: str) -> str:
    """
    Decrypt encrypted text.
    """
    decrypted_bytes = decrypt_bytes(encrypted_text)
    return decrypted_bytes.decode("utf-8")


def encrypt_image_bytes(image_bytes: bytes) -> str:
    """
    Encrypt image bytes.
    """
    return encrypt_bytes(image_bytes)


def decrypt_image_bytes(encrypted_image: str) -> bytes:
    """
    Decrypt encrypted image back into bytes.
    """
    return decrypt_bytes(encrypted_image)