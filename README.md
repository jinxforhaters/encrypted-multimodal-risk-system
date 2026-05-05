# Encrypted Multi-Modal Intelligence System

## 1. Project Overview

The Encrypted Multi-Modal Intelligence System is an AI/ML-powered risk analysis platform that accepts encrypted text and encrypted image data, decrypts the input using a custom reversible encryption pipeline, analyzes the text using NLP, analyzes the image using computer vision, and generates a unified risk score using a machine learning model.

The system provides:

- Custom encryption and decryption
- NLP-based text risk analysis
- Image anomaly / defect detection
- Unified ML-based risk scoring
- FastAPI backend
- MongoDB Atlas storage
- Streamlit dashboard
- Docker-based deployment setup

## 2. Problem Statement

The goal is to build a scalable system that processes encrypted multi-modal data consisting of:

- Text input
- Image input

The system decrypts both inputs, performs AI/ML analysis, generates a unified risk score, stores the result, and displays insights on a dashboard.

## 3. System Architecture

```text
User / Dashboard
      |
      | Encrypted Text + Encrypted Image
      v
FastAPI Backend
      |
      v
Custom Decryption Module
      |
      |-----------------------------|
      |                             |
      v                             v
NLP Processor                  Image Processor
Sentiment Analysis             OpenCV Anomaly Detection
Keyword Extraction             Defect Region Detection
Risk Keyword Detection         Image Anomaly Score
      |                             |
      |-------------|---------------|
                    v
          Feature Engineering Layer
                    |
                    v
          Risk Scoring ML Model
          Random Forest Classifier
                    |
                    v
          Unified Risk Score
                    |
                    v
          MongoDB Atlas Storage
                    |
                    v
          Streamlit Dashboard
```

## 4. Tech Stack

Backend:
- Python
- FastAPI
- Uvicorn
- Pydantic

AI/ML:
- Scikit-learn
- Random Forest Classifier
- OpenCV
- NumPy

Database:
- MongoDB Atlas
- PyMongo

Dashboard:
- Streamlit
- Plotly
- Requests

Deployment:
- Docker
- Docker Compose
- Render
- Kubernetes manifests included as bonus

## 5. Custom Encryption Pipeline

The project does not directly rely only on AES or Fernet. It uses a custom reversible encryption pipeline.

Encryption flow:

```text
Original text/image bytes
        |
        v
XOR with secret key
        |
        v
Byte shifting
        |
        v
Byte scrambling
        |
        v
Base64 encoding
        |
        v
Encrypted string
```

Decryption flow:

```text
Encrypted Base64 string
        |
        v
Base64 decoding
        |
        v
Unscrambling
        |
        v
Reverse byte shifting
        |
        v
XOR with same secret key
        |
        v
Original text/image bytes
```

Supported inputs:
- Text string
- Image bytes

Both text and image are converted into bytes before encryption.

## 6. NLP Processing

The NLP module performs:

- Sentiment analysis
- Keyword extraction
- Risk keyword detection
- Text risk score generation

Example NLP output:

```json
{
  "sentiment": "negative",
  "sentiment_score": 0.998,
  "keywords": ["machine", "overheating", "abnormal", "vibration"],
  "risk_keywords": ["overheating", "abnormal", "vibration"],
  "risk_keyword_count": 3,
  "text_risk_score": 0.78
}
```

## 7. Image Processing

The image processor performs OpenCV-based anomaly / defect detection.

Extracted image features include:

- Blur score
- Edge density
- Dark region ratio
- Bright region ratio
- Defect region count
- Image anomaly score

Example image output:

```json
{
  "image_anomaly_score": 0.67,
  "defect_detected": true,
  "defect_region_count": 4,
  "edge_density": 0.19,
  "dark_region_ratio": 0.08,
  "bright_region_ratio": 0.03
}
```

## 8. Risk Scoring Model

The final risk model combines NLP and image features.

Model used:
- Random Forest Classifier

Input features:
- `text_risk_score`
- `risk_keyword_count`
- `sentiment_score`
- `image_anomaly_score`
- `defect_region_count`
- `edge_density`
- `dark_region_ratio`
- `bright_region_ratio`

Output:

```json
{
  "risk_score": 0.86,
  "risk_level": "High",
  "model_confidence": 0.78,
  "class_probabilities": {
    "low": 0.02,
    "medium": 0.20,
    "high": 0.78
  }
}
```

Note: The current model is trained on synthetic data for demonstration. In production, this should be replaced with real labeled historical risk records.

## 9. Database Storage

MongoDB Atlas stores the following fields:

- `decrypted_text`
- `image_path`
- `nlp_result`
- `image_result`
- `risk_result`
- `risk_score`
- `risk_level`
- `timestamp`

Example MongoDB record:

```json
{
  "decrypted_text": "The machine is overheating and producing abnormal vibration.",
  "image_path": "uploads/sample.jpg",
  "risk_score": 0.86,
  "risk_level": "High",
  "timestamp": "2026-05-05T10:30:00Z"
}
```

## 10. API Endpoints

### Health Check

`GET /health`

Response:

```json
{
  "status": "healthy"
}
```

### Encrypt Text

`POST /encrypt-text`

Request:

```json
{
  "text": "The machine is overheating."
}
```

Response:

```json
{
  "encrypted_text": "encrypted_base64_string"
}
```

### Decrypt Text

`POST /decrypt-text`

Request:

```json
{
  "encrypted_text": "encrypted_base64_string"
}
```

Response:

```json
{
  "decrypted_text": "The machine is overheating."
}
```

### Analyze Encrypted Multi-Modal Data

`POST /analyze`

Request:

```json
{
  "encrypted_text": "encrypted_text_string",
  "encrypted_image": "encrypted_image_base64_string"
}
```

Response:

```json
{
  "record_id": "mongodb_record_id",
  "decrypted_text": "The machine is overheating and producing abnormal vibration.",
  "nlp_result": {
    "sentiment": "negative",
    "sentiment_score": 0.99,
    "keywords": ["machine", "overheating", "vibration"],
    "risk_keywords": ["overheating", "vibration"],
    "risk_keyword_count": 2,
    "text_risk_score": 0.76
  },
  "image_result": {
    "image_path": "uploads/image.jpg",
    "image_anomaly_score": 0.65,
    "defect_detected": true,
    "defect_region_count": 3
  },
  "risk_result": {
    "risk_score": 0.82,
    "risk_level": "High",
    "model_confidence": 0.74,
    "class_probabilities": {
      "low": 0.03,
      "medium": 0.23,
      "high": 0.74
    }
  }
}
```

### Get Recent Records

`GET /records?limit=20`

Response:

```json
{
  "records": [
    {
      "_id": "mongodb_record_id",
      "decrypted_text": "The machine is overheating.",
      "image_path": "uploads/image.jpg",
      "risk_score": 0.82,
      "risk_level": "High",
      "timestamp": "2026-05-05T10:30:00Z"
    }
  ]
}
```

## 11. Local Setup

Clone repository:

```bash
git clone <your-github-repo-url>
cd encrypted_multimodal_risk_system
```

Backend setup:

```bash
cd backend
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` inside `backend/`:

```env
MONGO_URI=mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=encrypted_multimodal_db
MONGO_COLLECTION_NAME=risk_records
```

Train risk model if `backend/models/risk_model.pkl` is missing:

```bash
python train_risk_model.py
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

Dashboard setup from project root:

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/streamlit_app.py
```

Dashboard runs at:

```text
http://localhost:8501
```

## 12. Docker Setup

Run both backend and dashboard:

```bash
docker compose up --build
```

Backend:

```text
http://127.0.0.1:8000/docs
```

Dashboard:

```text
http://127.0.0.1:8501
```

Stop containers:

```bash
docker compose down
```

## 13. Deployment

Backend can be deployed on Render.

Required backend environment variables:

```env
MONGO_URI=<your_mongodb_atlas_uri>
MONGO_DB_NAME=encrypted_multimodal_db
MONGO_COLLECTION_NAME=risk_records
```

Backend start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Dashboard can be deployed on Render or Streamlit Cloud.

Required dashboard environment variable:

```env
API_BASE_URL=https://your-backend-url.onrender.com
```

Dashboard start command:

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port $PORT
```

Deployment links:

- Backend: `<add deployed backend URL>`
- Dashboard: `<add deployed dashboard URL>`

## 14. Bonus Features Included

- Dockerized backend
- Dockerized dashboard
- Docker Compose setup
- Kubernetes deployment manifests
- MongoDB Atlas integration
- API-based architecture
- Explainable AI/ML risk features

## 15. Future Improvements

- Replace synthetic training data with real labeled data
- Add autoencoder-based image anomaly detection
- Add Celery + Redis async processing
- Add CI/CD pipeline using GitHub Actions
- Add JWT authentication
- Add real-time streaming pipeline
- Add image heatmap visualization for defect regions
