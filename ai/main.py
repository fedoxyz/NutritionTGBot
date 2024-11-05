# main.py
from typing import Callable, TypeVar
from pipelines import create_vision_pipeline, create_classification_pipeline
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

# Create lazy-loaded pipelines
process_receipt = create_lazy_pipeline(
    lambda: create_vision_pipeline()
)

classify_receipt_products = create_lazy_pipeline(
    lambda: create_classification_pipeline()
)

result = process_receipt("strewr")
print(result)
