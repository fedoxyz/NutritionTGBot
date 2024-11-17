from typing import Callable, Dict, TypeVar, List
from models import create_vision_model, create_classification_model
from utils import ProcessingResult, resize_image_bytes
from inference import process_image_with_model, classify_products_with_llm
from functools import lru_cache

T = TypeVar('T')  # Input type
R = TypeVar('R')  # Result type

def create_lazy_pipeline(
    creator: Callable[[], Callable[[T], R]]
) -> Callable[[T], R]:
    """Create a lazy-loaded pipeline with caching."""
    
    @lru_cache(maxsize=1)
    def get_pipeline() -> Callable[[T], R]:
        return creator()
    
    def pipeline(input_data: T) -> R:
        return get_pipeline()(input_data)
    
    return pipeline

def create_vision_pipeline() -> Callable[[bytes], ProcessingResult]:
    """Create vision pipeline for receipt processing."""
    model = create_vision_model()

    def vision_pipeline(input_data: bytes) -> ProcessingResult:
        #input_data = resize_image_bytes(input_data)
        return process_image_with_model(input_data, model)

    return vision_pipeline

def create_classification_pipeline() -> Callable[[Dict], ProcessingResult]:
    """Create classification pipeline for receipt products."""
    model = create_classification_model()

    return lambda receipt_data: classify_products_with_llm(receipt_data, model)

process_receipt = create_lazy_pipeline(
    lambda: create_vision_pipeline()
)

classify_receipt_products = create_lazy_pipeline(
    lambda: create_classification_pipeline()
)

