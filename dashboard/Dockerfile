FROM python:3.10-slim

WORKDIR /app

COPY dashboard/requirements.txt ./dashboard/requirements.txt

RUN pip install --no-cache-dir -r dashboard/requirements.txt

COPY dashboard ./dashboard

ENV API_BASE_URL=http://backend:8000

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
