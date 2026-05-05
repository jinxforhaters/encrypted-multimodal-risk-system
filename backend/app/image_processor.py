import os
import uuid
from typing import Dict, Any, Tuple

import cv2
import numpy as np


UPLOAD_DIR = "uploads"


class ImageProcessor:
    def __init__(self, upload_dir: str = UPLOAD_DIR):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def bytes_to_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Convert image bytes into OpenCV image.
        """
        if not image_bytes:
            raise ValueError("Image bytes cannot be empty.")

        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Invalid image data. Could not decode image.")

        return image

    def save_image(self, image: np.ndarray) -> str:
        """
        Save image to uploads folder and return image path.
        """
        filename = f"{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(self.upload_dir, filename)

        cv2.imwrite(image_path, image)

        return image_path

    def calculate_blur_score(self, gray: np.ndarray) -> float:
        """
        Variance of Laplacian:
        Lower value means image is blurrier.
        Higher value means sharper image.
        """
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        return float(blur_score)

    def calculate_edge_density(self, gray: np.ndarray) -> float:
        """
        Canny edge detection.
        Edge density = edge pixels / total pixels.
        """
        edges = cv2.Canny(gray, 100, 200)
        edge_pixels = np.count_nonzero(edges)
        total_pixels = gray.shape[0] * gray.shape[1]

        return float(edge_pixels / total_pixels)

    def calculate_dark_bright_ratios(self, gray: np.ndarray) -> Tuple[float, float]:
        """
        Dark region ratio: pixels very close to black.
        Bright region ratio: pixels very close to white.
        """
        total_pixels = gray.shape[0] * gray.shape[1]

        dark_pixels = np.sum(gray < 40)
        bright_pixels = np.sum(gray > 220)

        dark_ratio = dark_pixels / total_pixels
        bright_ratio = bright_pixels / total_pixels

        return float(dark_ratio), float(bright_ratio)

    def detect_defect_regions(self, gray: np.ndarray) -> int:
        """
        Basic defect detection using thresholding + contours.
        This detects suspicious high-contrast regions.
        """
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        thresholded = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            21,
            5
        )

        contours, _ = cv2.findContours(
            thresholded,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        defect_count = 0

        image_area = gray.shape[0] * gray.shape[1]

        for contour in contours:
            area = cv2.contourArea(contour)

            # Ignore very tiny noise and very large background regions
            if 100 < area < image_area * 0.20:
                defect_count += 1

        return int(defect_count)

    def normalize_features(
        self,
        blur_score: float,
        edge_density: float,
        dark_ratio: float,
        bright_ratio: float,
        defect_region_count: int
    ) -> Dict[str, float]:
        """
        Convert raw image features into normalized risk-like scores.
        Each score should be between 0 and 1.
        """

        # Low blur score means blurry image, which increases risk.
        blur_risk = 1.0 - min(blur_score / 500.0, 1.0)

        # Higher edge density can indicate cracks/scratches/noise.
        edge_risk = min(edge_density / 0.30, 1.0)

        # Too many dark or bright pixels can indicate abnormal regions.
        dark_risk = min(dark_ratio / 0.30, 1.0)
        bright_risk = min(bright_ratio / 0.30, 1.0)

        # More detected regions means more possible defects.
        defect_risk = min(defect_region_count / 10.0, 1.0)

        return {
            "blur_risk": round(float(blur_risk), 4),
            "edge_risk": round(float(edge_risk), 4),
            "dark_risk": round(float(dark_risk), 4),
            "bright_risk": round(float(bright_risk), 4),
            "defect_risk": round(float(defect_risk), 4)
        }

    def calculate_image_anomaly_score(self, normalized_features: Dict[str, float]) -> float:
        """
        Weighted image anomaly score.
        """
        score = (
            0.20 * normalized_features["blur_risk"] +
            0.25 * normalized_features["edge_risk"] +
            0.15 * normalized_features["dark_risk"] +
            0.15 * normalized_features["bright_risk"] +
            0.25 * normalized_features["defect_risk"]
        )

        return round(float(score), 4)

    def process_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Main function:
        image bytes -> OpenCV image -> image features -> anomaly score.
        """
        image = self.bytes_to_image(image_bytes)
        image_path = self.save_image(image)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blur_score = self.calculate_blur_score(gray)
        edge_density = self.calculate_edge_density(gray)
        dark_ratio, bright_ratio = self.calculate_dark_bright_ratios(gray)
        defect_region_count = self.detect_defect_regions(gray)

        normalized_features = self.normalize_features(
            blur_score=blur_score,
            edge_density=edge_density,
            dark_ratio=dark_ratio,
            bright_ratio=bright_ratio,
            defect_region_count=defect_region_count
        )

        image_anomaly_score = self.calculate_image_anomaly_score(normalized_features)

        defect_detected = image_anomaly_score >= 0.50 or defect_region_count >= 3

        return {
            "image_path": image_path,
            "blur_score": round(float(blur_score), 4),
            "edge_density": round(float(edge_density), 4),
            "dark_region_ratio": round(float(dark_ratio), 4),
            "bright_region_ratio": round(float(bright_ratio), 4),
            "defect_region_count": defect_region_count,
            "normalized_features": normalized_features,
            "image_anomaly_score": image_anomaly_score,
            "defect_detected": bool(defect_detected)
        }