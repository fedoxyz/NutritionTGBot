from langchain_ollama import ChatOllama
from functools import partial

ModelConfig = dict[str, str | float]

def create_base_model_config(
    format: str = "json",
    temperature: float = 0
) -> ModelConfig:
    """Create base model configuration."""
    return {
        "format": format,
        "keep_alive": -1,
        "temperature": temperature
    }

def create_model(
    model_id: str,
    config: ModelConfig
) -> ChatOllama:
    """Create a model with given configuration."""
    return ChatOllama(
        model=model_id,
        base_url="http://ollama-container:11434",
        **config
    )

create_vision_model = partial(
    create_model,
    model_id="llama3.2-vision",
    config=create_base_model_config()
)

create_classification_model = partial(
    create_model,
    model_id="llama3.2",
    config=create_base_model_config()
)
