# Product Requirements Document

## Product Name

Encrypted Multi-Modal Intelligence System

## Objective

Build a scalable API-based system that accepts encrypted multi-modal input, decrypts it through a custom reversible pipeline, processes text and image data, and generates unified risk insights through an ML-based risk score and dashboard.

## Problem Statement

Organizations often receive sensitive text and image data that must be processed securely before analytical insights can be generated. This product must demonstrate an end-to-end workflow where encrypted text and image inputs are decrypted, analyzed through NLP and computer vision techniques, converted into risk features, scored by a machine learning model, stored with metadata, and presented through a simple dashboard.

## Users

- Reviewer or evaluator testing the technical assignment
- Analyst reviewing submitted text/image risk records
- Developer maintaining the API, model, and dashboard workflow

## Core Requirements

### 1. Encrypted Input

The system must accept encrypted input for:

- Text as a string
- Image as base64 or uploaded file

### 2. Custom Encryption and Decryption

The encryption module must not rely only on AES, Fernet, or any direct library-only solution.

The encryption pipeline must include:

- Custom transformation logic such as XOR, shifting, or scrambling
- Base64 encoding
- A reversible encryption and decryption process

Required functions:

- `encrypt`
- `decrypt`

### 3. Text Processing

The system must perform NLP analysis on decrypted text.

Required text capabilities:

- Sentiment analysis
- Keyword extraction or entity recognition
- Risk keyword detection

Allowed libraries:

- `transformers`
- `nltk`
- `spacy`

### 4. Image Processing

The system must perform one computer vision analysis path on decrypted image input.

Required image capability:

- Anomaly detection, preferred
- Or defect detection

Allowed approaches:

- OpenCV for basic implementation
- PyTorch for advanced implementation
- Autoencoder for bonus implementation

### 5. Risk Scoring Model

The product must generate one unified risk score using features derived from:

- NLP output
- Image anomaly or defect score
- Any additional derived features

Allowed model options:

- Logistic Regression
- Random Forest
- XGBoost

### 6. API System

The backend must expose an API using:

- FastAPI, preferred for this project
- Or Flask

The API must support:

- Encrypted text submission
- Encrypted image submission
- Risk scoring response
- Recent record retrieval for dashboard usage

### 7. Data Storage

The system should use MongoDB Atlas as the recommended database.

Records stored in the database must include:

- Decrypted text
- Image path
- Risk score
- Timestamp

### 8. Dashboard

The dashboard must show:

- Risk score
- Recent records
- Basic visualization

## Functional Requirements

### Text Risk Flow

1. User submits encrypted text to the API.
2. API decrypts the text using the custom decryption pipeline.
3. NLP processor extracts sentiment, keywords/entities, and risk keyword matches.
4. Risk model receives text features.
5. API returns risk score and stores the record.

### Image Risk Flow

1. User submits encrypted image data as base64 or file.
2. API decrypts and decodes the image.
3. Image processor performs anomaly or defect detection.
4. Risk model receives image features.
5. API returns risk score and stores the image path and metadata.

### Unified Risk Flow

1. System combines text features, image features, and derived metadata.
2. ML model predicts a unified risk score.
3. Score is returned through the API and displayed in the dashboard.

## Non-Functional Requirements

- The system must be scalable and API queryable.
- Encryption and decryption must be reversible and demonstrable.
- The project must show internal logic and must not depend on black-box APIs.
- The implementation must be original and not copied from GitHub projects or end-to-end tutorials.
- README must include complete setup details, API examples, and architecture explanation.

## Deployment Requirements

Expected deployment targets:

- Backend API: Render
- Database: MongoDB Atlas
- Dashboard: deployable separately, such as Streamlit Community Cloud or another compatible host

## Bonus Requirements

The following are bonus items:

- Async processing with Celery and Redis
- Docker deployment
- Kubernetes deployment
- CI/CD pipeline
- Advanced anomaly detection
- Real-time streaming

## Deliverables

- GitHub repository
- Working deployed links
- Complete `README.md`
- Architecture explanation in README or PDF
- API request and response examples
- Source code for backend, dashboard, model training, encryption, NLP, image processing, and storage

## Suggested API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/encrypt/text` | Encrypt plain text for testing |
| `POST` | `/decrypt/text` | Decrypt encrypted text for testing |
| `POST` | `/risk/text` | Submit encrypted text and receive risk score |
| `POST` | `/risk/image` | Submit encrypted image and receive risk score |
| `GET` | `/records` | Fetch recent stored records |
| `GET` | `/health` | Check API health |

## Success Criteria

- API accepts encrypted text and image inputs.
- Custom encryption and decryption pipeline works end to end.
- Text processor returns sentiment, keywords/entities, and risk keyword matches.
- Image processor returns anomaly or defect score.
- ML model returns a unified risk score.
- MongoDB stores required fields.
- Dashboard displays score, recent records, and basic visualization.
- README provides clear setup, architecture, and API usage.

## Timeline

The expected implementation timeline from the assignment is 12 hours.
