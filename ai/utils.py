from typing import Any
import pickle
import numpy as np
import json
import torch
import torch.nn.functional as F
from logger import logger

class ProcessingResult:
    def __init__(self, success: bool, data: Any, error: str = ""):
        self.success = success
        self.data = data
        self.error = error

    def __str__(self):
        if self.success:
            return f"Success: {self.success}"
        else:
            return f"Failed: {self.error}"

from typing import Union
from PIL import Image
import io

def resize_image_bytes(image_bytes: Union[bytes, bytearray], max_size: int = 1120) -> bytes:
    # Open the image from bytes
    image = Image.open(io.BytesIO(image_bytes))

    # Resize while preserving the aspect ratio
    image.thumbnail((max_size, max_size), Image.LANCZOS)
    # Save the resized image to bytes
    output_bytes = io.BytesIO()
    image.save(output_bytes, format="JPEG")  # Adjust format if needed
    output_bytes.seek(0)

    return output_bytes.getvalue()  # Return the resized image bytes


def pickle_load(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)


def postprocess_keras_preds(preds):
    labels = np.argmax(preds, axis = -1)
    categories = pickle_load("categories.pkl")
    confidence = [round(pred[labels[i]] * 100, 2) for i, pred in enumerate(preds)]
    results = [categories[label] for label in labels]
    for category, conf in zip(results, confidence):
        logger.debug(f"{category:<65}||   {conf:^10.2f}")
    return json.dumps(results, ensure_ascii=False)

def postprocess_bert_preds(preds):
    logits = preds.logits
    probabilities = F.softmax(torch.tensor(logits), dim=-1).numpy()
    confidence = np.max(probabilities, axis=1)
    id2label = pickle_load("id2label.pkl")
    pred_labels = np.argmax(probabilities, axis=-1)
    pred_categories = [id2label[label] for label in pred_labels]
    for category, conf in zip(pred_categories, confidence):
        logger.debug(f"{category:<65}||   {conf:^10.2f}")

    return json.dumps(pred_categories, ensure_ascii=False)
