from typing import Any, Dict, List
from pydantic import BaseModel


class EncryptTextRequest(BaseModel):
    text: str


class EncryptTextResponse(BaseModel):
    encrypted_text: str


class DecryptTextRequest(BaseModel):
    encrypted_text: str


class DecryptTextResponse(BaseModel):
    decrypted_text: str


class AnalyzeRequest(BaseModel):
    encrypted_text: str
    encrypted_image: str


class AnalyzeResponse(BaseModel):
    record_id: str
    decrypted_text: str
    nlp_result: Dict[str, Any]
    image_result: Dict[str, Any]
    risk_result: Dict[str, Any]


class RecentRecordsResponse(BaseModel):
    records: List[Dict[str, Any]]
