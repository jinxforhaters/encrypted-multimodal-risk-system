from datetime import datetime, timezone
from typing import Any, Dict, List

import certifi
from pymongo import DESCENDING, MongoClient

from app.config import settings


class MongoDBClient:
    def __init__(self):
        if not settings.MONGO_URI:
            raise ValueError("MONGO_URI is missing. Please add it in backend/.env")

        self.client = MongoClient(
            settings.MONGO_URI,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=30000
        )
        self.db = self.client[settings.MONGO_DB_NAME]
        self.collection = self.db[settings.MONGO_COLLECTION_NAME]

    def insert_risk_record(
        self,
        decrypted_text: str,
        image_path: str,
        nlp_result: Dict[str, Any],
        image_result: Dict[str, Any],
        risk_result: Dict[str, Any]
    ) -> str:
        record = {
            "decrypted_text": decrypted_text,
            "image_path": image_path,
            "nlp_result": nlp_result,
            "image_result": image_result,
            "risk_result": risk_result,
            "risk_score": risk_result.get("risk_score"),
            "risk_level": risk_result.get("risk_level"),
            "timestamp": datetime.now(timezone.utc)
        }

        result = self.collection.insert_one(record)
        return str(result.inserted_id)

    def get_recent_records(self, limit: int = 20) -> List[Dict[str, Any]]:
        records = list(
            self.collection
            .find({})
            .sort("timestamp", DESCENDING)
            .limit(limit)
        )

        for record in records:
            record["_id"] = str(record["_id"])
            if "timestamp" in record and record["timestamp"]:
                record["timestamp"] = record["timestamp"].isoformat()

        return records
