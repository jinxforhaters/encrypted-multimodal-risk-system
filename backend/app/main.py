from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    EncryptTextRequest,
    EncryptTextResponse,
    DecryptTextRequest,
    DecryptTextResponse,
    AnalyzeRequest,
    AnalyzeResponse,
    RecentRecordsResponse
)

from app.encryption import (
    encrypt_text,
    decrypt_text,
    decrypt_image_bytes
)

from app.nlp_processor import NLPProcessor
from app.image_processor import ImageProcessor
from app.risk_model import RiskScoringModel
from app.database import MongoDBClient


db_client = None


def get_db_client() -> MongoDBClient:
    global db_client

    if db_client is None:
        db_client = MongoDBClient()

    return db_client


app = FastAPI(
    title="Encrypted Multi-Modal Intelligence System",
    description="API for encrypted text + image analysis and unified risk scoring.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


nlp_processor = NLPProcessor()
image_processor = ImageProcessor()
risk_model = RiskScoringModel()


@app.get("/")
def root():
    return {
        "message": "Encrypted Multi-Modal Intelligence System API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/encrypt-text", response_model=EncryptTextResponse)
def encrypt_text_endpoint(request: EncryptTextRequest):
    try:
        encrypted = encrypt_text(request.text)
        return {
            "encrypted_text": encrypted
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/decrypt-text", response_model=DecryptTextResponse)
def decrypt_text_endpoint(request: DecryptTextRequest):
    try:
        decrypted = decrypt_text(request.encrypted_text)
        return {
            "decrypted_text": decrypted
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_encrypted_multimodal_data(request: AnalyzeRequest):
    try:
        # 1. Decrypt text
        decrypted_text = decrypt_text(request.encrypted_text)

        # 2. Decrypt image
        decrypted_image_bytes = decrypt_image_bytes(request.encrypted_image)

        # 3. NLP processing
        nlp_result = nlp_processor.process_text(decrypted_text)

        # 4. Image processing
        image_result = image_processor.process_image(decrypted_image_bytes)

        # 5. Final ML risk scoring
        risk_result = risk_model.predict_risk(
            nlp_result=nlp_result,
            image_result=image_result
        )

        # 6. Store complete analysis result in MongoDB
        record_id = get_db_client().insert_risk_record(
            decrypted_text=decrypted_text,
            image_path=image_result.get("image_path", ""),
            nlp_result=nlp_result,
            image_result=image_result,
            risk_result=risk_result
        )

        return {
            "record_id": record_id,
            "decrypted_text": decrypted_text,
            "nlp_result": nlp_result,
            "image_result": image_result,
            "risk_result": risk_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/records", response_model=RecentRecordsResponse)
def get_recent_records(limit: int = 20):
    try:
        records = get_db_client().get_recent_records(limit=limit)
        return {
            "records": records
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
