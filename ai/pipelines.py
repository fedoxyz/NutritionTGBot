from typing import Callable, Dict
from models import create_vision_model, create_classification_model
from utils import ProcessingResult
from inference import process_image_with_model, classify_products_with_llm

def create_vision_pipeline() -> Callable[[bytes], ProcessingResult]:
    """Create vision pipeline for receipt processing."""
    model = create_vision_model()

    def vision_pipeline(input_data: bytes) -> ProcessingResult:
        return process_image_with_model(input_data, model)

    return vision_pipeline

def create_classification_pipeline() -> Callable[[Dict], ProcessingResult]:
    """Create classification pipeline for receipt products"""
    model = create_classification_model()

    return lambda receipt_data: classify_products_with_llm(model, receipt_data)
