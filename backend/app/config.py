import os
from pathlib import Path

from dotenv import load_dotenv


ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)


class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "encrypted_multimodal_db")
    MONGO_COLLECTION_NAME: str = os.getenv("MONGO_COLLECTION_NAME", "risk_records")


settings = Settings()
