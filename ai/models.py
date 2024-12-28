from langchain_ollama import ChatOllama
from functools import partial
from tensorflow.keras.models import load_model
from logger import logger
from transformers import BertForSequenceClassification, BertTokenizer
from typing import Tuple
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

OllamaConfig = dict[str, str | float]

def create_ollama_model_config(
    format: str = "json",
    temperature: float = 0,
) -> OllamaConfig:
    """Create base model configuration."""
    return {
        "format": format,
        "keep_alive": -1,
        "temperature": temperature,
        "num_ctx": 32000
    }

def create_ollama_model(
    model_id: str,
    config: OllamaConfig
) -> ChatOllama:
    """Create a model with given configuration."""
    return ChatOllama(
        model=model_id,
        base_url="http://ollama-container:11434",
        **config
    )





def create_keras_model(file_path):
    logger.debug(f"Loading keras model from {file_path}")
    return load_model(file_path) 







def create_bert_model(path) -> Tuple[BertForSequenceClassification, BertTokenizer]:
    logger.debug("Creating BERT model")
    # Загрузка сохраненной модели и токенизатора
    model = BertForSequenceClassification.from_pretrained(path).to(device)
    tokenizer = BertTokenizer.from_pretrained(path)
    return model, tokenizer







create_vision_model = partial(
    create_ollama_model,
    model_id="llama3.2-vision",
    config=create_ollama_model_config()
)

create_classification_ollama_model = partial(
    create_ollama_model,
    model_id="llama3.2",
    config=create_ollama_model_config()
)



