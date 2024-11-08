from typing import Callable, TypeVar, Any, Union
from prompts import create_classification_prompt, create_vision_prompt
from utils import ProcessingResult
from pydantic_schemas import Receipt, ClassifiedProduct
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import AIMessage
import json
import traceback
from logger import logger

T = TypeVar('T')  # Input type

def create_inference_function(
    prompt_generator: Callable[[T], str],
    parser: JsonOutputParser,
    parse_multiple: bool = False
) -> Callable[[T, Any], ProcessingResult]:
    """Create an inference function with proper response handling."""
    
    def extract_content(response: Union[str, AIMessage]) -> str:
        """Extract content string from various response types."""
        if isinstance(response, AIMessage):
            return response.content
        return response
    
    def process_with_model(input_data: T, model: Any) -> ProcessingResult:
        try:
            prompt = prompt_generator(input_data)
            logger.debug(f"prompt - {prompt}")
            response = model.invoke(prompt)
            logger.debug(response)
            logger.debug(dir(response))
            # Extract content from response
            content = extract_content(response)
            # Ensure content is valid JSON
            if not content.strip().startswith('{'):
                raise ValueError(f"Invalid JSON response: {content[:100]}...")
                
            if parse_multiple:
                try:
                    json_data = json.loads(content)
                    if not isinstance(json_data, list):
                        json_data = [json_data]
                    result = [parser.parse(json.dumps(item)) for item in json_data]
                except json.JSONDecodeError as e:
                    raise ValueError(f"Failed to parse JSON response: {str(e)}")
            else:
                result = parser.parse(content)
                
            return ProcessingResult(True, result)
            
        except Exception as e:
            error_msg = f"Error processing inference: {str(e)}\n{traceback.format_exc()}"
            return ProcessingResult(False, None, error_msg)
    
    return process_with_model

# Create specialized inference functions
process_image_with_model = create_inference_function(
    prompt_generator=create_vision_prompt,
    parser=JsonOutputParser(pydantic_object=Receipt)
)

classify_products_with_llm = create_inference_function(
    prompt_generator=create_classification_prompt,
    parser=JsonOutputParser(pydantic_object=ClassifiedProduct),
    parse_multiple=True
)
