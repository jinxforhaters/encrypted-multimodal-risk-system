import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "risk_model.pkl")


def generate_synthetic_data(n_samples: int = 2000) -> pd.DataFrame:
    """
    Generate synthetic training data for the risk scoring model.

    In a real-world system, these labels should come from actual historical
    inspection/risk records.
    """
    np.random.seed(42)

    data = []

    for _ in range(n_samples):
        text_risk_score = np.random.uniform(0, 1)
        risk_keyword_count = np.random.randint(0, 10)
        sentiment_score = np.random.uniform(0, 1)

        image_anomaly_score = np.random.uniform(0, 1)
        defect_region_count = np.random.randint(0, 12)
        edge_density = np.random.uniform(0, 0.35)
        dark_region_ratio = np.random.uniform(0, 0.4)
        bright_region_ratio = np.random.uniform(0, 0.4)

        # Rule-based synthetic risk logic
        combined_score = (
            0.35 * text_risk_score +
            0.15 * min(risk_keyword_count / 10, 1.0) +
            0.30 * image_anomaly_score +
            0.10 * min(defect_region_count / 10, 1.0) +
            0.05 * min(edge_density / 0.35, 1.0) +
            0.025 * min(dark_region_ratio / 0.4, 1.0) +
            0.025 * min(bright_region_ratio / 0.4, 1.0)
        )

        # Convert combined score into class label
        # 0 = Low, 1 = Medium, 2 = High
        if combined_score < 0.35:
            risk_label = 0
        elif combined_score < 0.70:
            risk_label = 1
        else:
            risk_label = 2

        data.append({
            "text_risk_score": text_risk_score,
            "risk_keyword_count": risk_keyword_count,
            "sentiment_score": sentiment_score,
            "image_anomaly_score": image_anomaly_score,
            "defect_region_count": defect_region_count,
            "edge_density": edge_density,
            "dark_region_ratio": dark_region_ratio,
            "bright_region_ratio": bright_region_ratio,
            "risk_label": risk_label
        })

    return pd.DataFrame(data)


def train_model():
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = generate_synthetic_data()

    feature_columns = [
        "text_risk_score",
        "risk_keyword_count",
        "sentiment_score",
        "image_anomaly_score",
        "defect_region_count",
        "edge_density",
        "dark_region_ratio",
        "bright_region_ratio"
    ]

    X = df[feature_columns]
    y = df["risk_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    joblib.dump(
        {
            "model": model,
            "feature_columns": feature_columns
        },
        MODEL_PATH
    )

    print(f"\nModel saved at: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()