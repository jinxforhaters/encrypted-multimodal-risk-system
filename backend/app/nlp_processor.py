import re
from collections import Counter
from typing import Dict, List, Any

from transformers import pipeline


RISK_KEYWORDS = [
    "risk", "danger", "dangerous", "failure", "failed", "fault", "faulty",
    "defect", "defective", "damage", "damaged", "crack", "cracked",
    "leak", "leakage", "broken", "corrosion", "corroded",
    "overheat", "overheating", "burn", "burning", "fire",
    "abnormal", "vibration", "noise", "contamination", "unsafe",
    "warning", "critical", "urgent", "hazard", "error"
]

STOPWORDS = {
    "the", "is", "are", "was", "were", "a", "an", "and", "or", "to",
    "of", "in", "on", "for", "with", "this", "that", "it", "as", "by",
    "from", "at", "be", "been", "has", "have", "had", "we", "they",
    "you", "i", "he", "she", "there", "here", "not", "but", "so"
}

class NLPProcessor:
    def __init__(self):
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def extract_keywords(self, text: str, top_k: int = 8) -> List[str]:
        cleaned_text = self.clean_text(text)
        words = cleaned_text.split()

        filtered_words = [
            word for word in words
            if word not in STOPWORDS and len(word) > 2
        ]

        word_counts = Counter(filtered_words)
        keywords = [word for word, _ in word_counts.most_common(top_k)]

        return keywords

    def detect_risk_keywords(self, text: str) -> List[str]:
        cleaned_text = self.clean_text(text)

        found_keywords = []
        for keyword in RISK_KEYWORDS:
            if keyword in cleaned_text:
                found_keywords.append(keyword)

        return found_keywords

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        result = self.sentiment_pipeline(text[:512])[0]

        label = result["label"].lower()
        score = float(result["score"])

        return {
            "sentiment": label,
            "sentiment_score": score
        }

    def calculate_text_risk_score(
        self,
        sentiment: str,
        sentiment_score: float,
        risk_keywords: List[str],
        text: str
    ) -> float:
        risk_keyword_score = min(len(risk_keywords) / 5, 1.0)

        if sentiment == "negative":
            sentiment_risk = sentiment_score
        else:
            sentiment_risk = 1 - sentiment_score

        length_score = min(len(text.split()) / 100, 1.0)

        final_score = (
            0.50 * risk_keyword_score +
            0.35 * sentiment_risk +
            0.15 * length_score
        )

        return round(float(final_score), 4)

    def process_text(self, text: str) -> Dict[str, Any]:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        sentiment_result = self.analyze_sentiment(text)
        keywords = self.extract_keywords(text)
        risk_keywords = self.detect_risk_keywords(text)

        text_risk_score = self.calculate_text_risk_score(
            sentiment=sentiment_result["sentiment"],
            sentiment_score=sentiment_result["sentiment_score"],
            risk_keywords=risk_keywords,
            text=text
        )

        return {
            "sentiment": sentiment_result["sentiment"],
            "sentiment_score": sentiment_result["sentiment_score"],
            "keywords": keywords,
            "risk_keywords": risk_keywords,
            "risk_keyword_count": len(risk_keywords),
            "text_risk_score": text_risk_score
        }
