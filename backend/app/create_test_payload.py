import json
from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.encryption import encrypt_text, encrypt_image_bytes


text = "The machine is overheating and producing abnormal vibration. There may be a critical defect."
ROOT_DIR = BACKEND_DIR.parent
default_image_path = BACKEND_DIR / "uploads" / "test_image.jpg"
fallback_image_path = ROOT_DIR / "tests" / "final_output.png"
image_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_image_path

if not image_path.exists() and fallback_image_path.exists():
    image_path = fallback_image_path

if not image_path.exists():
    raise FileNotFoundError(
        f"Image not found: {image_path}. Pass an image path as the first argument."
    )

with open(image_path, "rb") as f:
    image_bytes = f.read()

payload = {
    "encrypted_text": encrypt_text(text),
    "encrypted_image": encrypt_image_bytes(image_bytes)
}

print(json.dumps(payload, indent=2))
