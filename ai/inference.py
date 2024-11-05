from typing import Callable, TypeVar, Any
from prompts import create_classification_prompt, create_vision_prompt
from utils import ProcessingResult
from pydantic_schemas import Receipt, ClassifiedProduct
from langchain.output_parsers import PydanticOutputParser
import json

T = TypeVar('T')  # Input type

def create_inference_function(
    prompt_generator: Callable[[T], str],
    parser: PydanticOutputParser,
    parse_multiple: bool = False
) -> Callable[[T, Any], ProcessingResult]:
    """Create an inference function with error handling."""
    
    def process_with_model(input_data: T, model: Any) -> ProcessingResult:
        try:
            prompt = prompt_generator(input_data)
            response = model(prompt)
            
            if parse_multiple:
                result = [
                    parser.parse(item)
                    for item in json.loads(response)
                ]
            else:
                result = parser.parse(response)
                
            return ProcessingResult(True, result)
            
        except Exception as e:
            return ProcessingResult(False, None, str(e))
    
    return process_with_model

# Create specialized inference functions
process_image_with_model = create_inference_function(
    prompt_generator=create_vision_prompt,
    parser=PydanticOutputParser(pydantic_object=Receipt)
)

classify_products_with_llm = create_inference_function(
    prompt_generator=create_classification_prompt,
    parser=PydanticOutputParser(pydantic_object=ClassifiedProduct),
    parse_multiple=True
)
