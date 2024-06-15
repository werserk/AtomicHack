from typing import Optional, Dict

import cv2
import numpy as np
import streamlit as st
from supervision.detection.core import Detections

from app.neuro.roboflow_net import RoboflowModel, RoboflowVisualizer


@st.cache_resource
def get_model() -> RoboflowModel:
    return RoboflowModel()


@st.cache_resource
def get_visualizer() -> RoboflowVisualizer:
    return RoboflowVisualizer()


class Resizer:
    def __init__(self, size: Optional[tuple] = (640, 640)):
        self.size = size
        self.image_size = None

    def apply(self, image: np.ndarray) -> np.ndarray:
        self.image_size = image.shape[:2]
        return cv2.resize(image, self.size)

    def revert(self, image: np.ndarray, detections: Detections) -> Dict[str, np.array]:
        reverted_image = cv2.resize(image, (self.image_size[1], self.image_size[0]))
        coords = detections.xyxy
        coords[:, ::2] *= self.image_size[1] / self.size[0]
        coords[:, 1::2] *= self.image_size[0] / self.size[1]
        detections.xyxy = coords
        return {"image": reverted_image, "detections": detections}


class Processor:
    def __init__(self):
        self.predictor = get_model()
        self.visualizer = get_visualizer()
        self.resizer = Resizer()

    def __call__(self, image: np.ndarray) -> np.ndarray:
        resized_image = self.resizer.apply(image)
        predictions = self.predictor(resized_image)
        reverted = self.resizer.revert(image, predictions.detections)
        reverted_image = reverted["image"]
        predictions.detections = reverted["detections"]
        annotated_image = self.visualizer.plot_predictions(
            image=reverted_image, predictions=predictions
        )
        return annotated_image