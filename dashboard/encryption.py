import base64
from typing import ByteString


SECRET_KEY = "my_secret_key_123"
SHIFT_VALUE = 3


def _xor_bytes(data: bytes, key: str = SECRET_KEY) -> bytes:
    key_bytes = key.encode("utf-8")
    return bytes(
        byte ^ key_bytes[i % len(key_bytes)]
        for i, byte in enumerate(data)
    )


def _shift_bytes(data: bytes, shift: int = SHIFT_VALUE) -> bytes:
    return bytes((byte + shift) % 256 for byte in data)


def _scramble_bytes(data: bytes) -> bytes:
    even_bytes = data[::2]
    odd_bytes = data[1::2]
    return even_bytes + odd_bytes


def encrypt_bytes(data: ByteString) -> str:
    if not data:
        raise ValueError("Input data cannot be empty.")

    data = bytes(data)
    step_1 = _xor_bytes(data)
    step_2 = _shift_bytes(step_1)
    step_3 = _scramble_bytes(step_2)
    return base64.b64encode(step_3).decode("utf-8")


def encrypt_text(text: str) -> str:
    if not text:
        raise ValueError("Text cannot be empty.")

    return encrypt_bytes(text.encode("utf-8"))


def encrypt_image_bytes(image_bytes: bytes) -> str:
    return encrypt_bytes(image_bytes)
