from typing import Callable, Dict, TypeVar
from models import create_vision_model, create_keras_model, create_classification_ollama_model, create_bert_model
from utils import ProcessingResult 
from inference import process_image_with_model, classify_products_with_llm, classify_products_with_keras, classify_products_with_bert
from functools import lru_cache
from logger import logger
from sentence_transformers import SentenceTransformer

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

def create_ollama_classification_pipeline() -> Callable[[Dict], ProcessingResult]:
    """Create classification pipeline for receipt products."""
    model = create_classification_ollama_model()

    return lambda receipt_data: classify_products_with_llm(receipt_data, model)

def create_keras_classification_pipeline() -> Callable[[Dict], ProcessingResult]:
    """Create classification pipeline for receipt products."""
    logger.debug("Before loading model in Keras classification pipeline")
    model = create_keras_model("models/model.keras")
    st = SentenceTransformer("all-MiniLM-L6-v2") 
    logger.debug("Keras classification model created on first inference of pipeline")

    return lambda receipt_data: classify_products_with_keras(st.encode(receipt_data), model)

def create_bert_classification_pipeline() -> Callable[[Dict], ProcessingResult]:
    """Create classification pipeline for receipt products."""
    logger.debug("Before loading model in BERT classification pipeline")
    model, tokenizer = create_bert_model("models/bert")
    logger.debug("BERT classification model created on first inference of pipeline")

    return lambda receipt_data: classify_products_with_bert(tokenizer(receipt_data, return_tensors="pt", padding=True, truncation=True), model)


process_receipt = create_lazy_pipeline(
    lambda: create_vision_pipeline()
)

classify_ollama_receipt_products = create_lazy_pipeline(
    lambda: create_ollama_classification_pipeline()
)

classify_receipt_keras = create_lazy_pipeline(
        lambda: create_keras_classification_pipeline()
)

classify_receipt_bert = create_lazy_pipeline(
        lambda: create_bert_classification_pipeline()
)

