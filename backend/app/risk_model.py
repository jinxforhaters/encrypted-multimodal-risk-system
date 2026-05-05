import os
from typing import Dict, Any

import joblib


MODEL_PATH = os.path.join("models", "risk_model.pkl")


class RiskScoringModel:
    def __init__(self, model_path: str = MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Risk model not found at {model_path}. "
                "Please run: python train_risk_model.py"
            )

        model_data = joblib.load(model_path)

        self.model = model_data["model"]
        self.feature_columns = model_data["feature_columns"]

    def prepare_features(
        self,
        nlp_result: Dict[str, Any],
        image_result: Dict[str, Any]
    ) -> list[list[float]]:
        """
        Convert NLP + image outputs into model input features.
        """
        features = {
            "text_risk_score": nlp_result.get("text_risk_score", 0.0),
            "risk_keyword_count": nlp_result.get("risk_keyword_count", 0),
            "sentiment_score": nlp_result.get("sentiment_score", 0.0),
            "image_anomaly_score": image_result.get("image_anomaly_score", 0.0),
            "defect_region_count": image_result.get("defect_region_count", 0),
            "edge_density": image_result.get("edge_density", 0.0),
            "dark_region_ratio": image_result.get("dark_region_ratio", 0.0),
            "bright_region_ratio": image_result.get("bright_region_ratio", 0.0)
        }

        return [[features[column] for column in self.feature_columns]]

    def predict_risk(
        self,
        nlp_result: Dict[str, Any],
        image_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predict final risk level and risk score.
        """
        X = self.prepare_features(nlp_result, image_result)

        predicted_class = int(self.model.predict(X)[0])
        probabilities = self.model.predict_proba(X)[0]

        # Probability of predicted class
        confidence = float(probabilities[predicted_class])

        # Weighted continuous risk score
        # Low class contributes 0.2, Medium 0.6, High 1.0
        risk_score = (
            probabilities[0] * 0.2 +
            probabilities[1] * 0.6 +
            probabilities[2] * 1.0
        )

        risk_label_map = {
            0: "Low",
            1: "Medium",
            2: "High"
        }

        return {
            "risk_score": round(float(risk_score), 4),
            "risk_level": risk_label_map[predicted_class],
            "model_confidence": round(confidence, 4),
            "class_probabilities": {
                "low": round(float(probabilities[0]), 4),
                "medium": round(float(probabilities[1]), 4),
                "high": round(float(probabilities[2]), 4)
            }
        }
