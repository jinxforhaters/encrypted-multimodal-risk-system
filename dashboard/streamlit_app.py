import base64
import os
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from encryption import encrypt_image_bytes, encrypt_text


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


st.set_page_config(
    page_title="Encrypted Multi-Modal Risk Dashboard",
    page_icon="🔐",
    layout="wide"
)


st.title("🔐 Encrypted Multi-Modal Intelligence Dashboard")
st.write("Upload text and image data, encrypt it, analyze risk, and view recent records.")


def get_risk_badge(risk_level: str):
    if risk_level == "High":
        return "🔴 High"
    elif risk_level == "Medium":
        return "🟠 Medium"
    return "🟢 Low"


def analyze_payload(text: str, image_bytes: bytes):
    encrypted_text = encrypt_text(text)
    encrypted_image = encrypt_image_bytes(image_bytes)

    payload = {
        "encrypted_text": encrypted_text,
        "encrypted_image": encrypted_image
    }

    response = requests.post(
        f"{API_BASE_URL}/analyze",
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()


def fetch_recent_records(limit: int = 20):
    response = requests.get(
        f"{API_BASE_URL}/records",
        params={"limit": limit},
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json().get("records", [])


left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Input Data")

    input_text = st.text_area(
        "Enter text",
        value="The machine is overheating and producing abnormal vibration. There may be a critical defect.",
        height=160
    )

    uploaded_image = st.file_uploader(
        "Upload image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    analyze_button = st.button("Encrypt + Analyze", type="primary")

with right_col:
    st.subheader("Analysis Result")

    if analyze_button:
        if not input_text.strip():
            st.error("Please enter text.")
        elif uploaded_image is None:
            st.error("Please upload an image.")
        else:
            try:
                image_bytes = uploaded_image.read()

                with st.spinner("Encrypting and analyzing..."):
                    result = analyze_payload(input_text, image_bytes)

                risk_result = result["risk_result"]
                nlp_result = result["nlp_result"]
                image_result = result["image_result"]

                risk_score = risk_result["risk_score"]
                risk_level = risk_result["risk_level"]

                st.success("Analysis completed successfully.")

                metric_col1, metric_col2, metric_col3 = st.columns(3)

                with metric_col1:
                    st.metric("Risk Score", risk_score)

                with metric_col2:
                    st.metric("Risk Level", get_risk_badge(risk_level))

                with metric_col3:
                    st.metric("Model Confidence", risk_result["model_confidence"])

                st.progress(min(float(risk_score), 1.0))

                st.write("### NLP Insights")
                st.json({
                    "sentiment": nlp_result.get("sentiment"),
                    "sentiment_score": nlp_result.get("sentiment_score"),
                    "keywords": nlp_result.get("keywords"),
                    "risk_keywords": nlp_result.get("risk_keywords"),
                    "text_risk_score": nlp_result.get("text_risk_score")
                })

                st.write("### Image Insights")
                st.json({
                    "image_anomaly_score": image_result.get("image_anomaly_score"),
                    "defect_detected": image_result.get("defect_detected"),
                    "defect_region_count": image_result.get("defect_region_count"),
                    "edge_density": image_result.get("edge_density"),
                    "dark_region_ratio": image_result.get("dark_region_ratio"),
                    "bright_region_ratio": image_result.get("bright_region_ratio")
                })

                st.write("### Class Probabilities")
                probabilities = risk_result.get("class_probabilities", {})
                prob_df = pd.DataFrame({
                    "risk_level": list(probabilities.keys()),
                    "probability": list(probabilities.values())
                })

                fig = px.bar(
                    prob_df,
                    x="risk_level",
                    y="probability",
                    title="Risk Class Probabilities"
                )
                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Analysis failed: {e}")


st.divider()

st.subheader("Recent Risk Records")

record_limit = st.slider("Number of records", min_value=5, max_value=50, value=20)

try:
    records = fetch_recent_records(limit=record_limit)

    if not records:
        st.info("No records found yet.")
    else:
        table_rows = []

        for record in records:
            table_rows.append({
                "timestamp": record.get("timestamp"),
                "risk_score": record.get("risk_score"),
                "risk_level": record.get("risk_level"),
                "text": record.get("decrypted_text", "")[:100],
                "image_path": record.get("image_path")
            })

        df = pd.DataFrame(table_rows)

        st.dataframe(df, use_container_width=True)

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.write("### Risk Level Distribution")
            level_counts = df["risk_level"].value_counts().reset_index()
            level_counts.columns = ["risk_level", "count"]

            fig_level = px.bar(
                level_counts,
                x="risk_level",
                y="count",
                title="Risk Level Count"
            )
            st.plotly_chart(fig_level, use_container_width=True)

        with chart_col2:
            st.write("### Risk Score Trend")
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df_sorted = df.sort_values("timestamp")

            fig_score = px.line(
                df_sorted,
                x="timestamp",
                y="risk_score",
                title="Recent Risk Score Trend",
                markers=True
            )
            st.plotly_chart(fig_score, use_container_width=True)

except Exception as e:
    st.warning(f"Could not fetch recent records. Make sure FastAPI is running. Error: {e}")
