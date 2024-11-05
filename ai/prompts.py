import json
from typing import Dict, Callable, TypeVar, Type, Any
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from pydantic_schemas import Receipt, ClassifiedProduct

T = TypeVar('T', bound=BaseModel)

def create_parser_prompt(
    pydantic_model: Type[T],
    query_generator: Callable[[Any], str]
) -> Callable[[Any], str]:
    parser = PydanticOutputParser(pydantic_object=pydantic_model)
    format_instructions = parser.get_format_instructions()
    
    prompt_template = PromptTemplate(
        template="Answer the query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": format_instructions},
    )
    
    def generate_prompt(input_data: Any) -> str:
        return prompt_template.format(query=query_generator(input_data))
    
    return generate_prompt

# Query generator functions
def generate_classification_query(receipt_json: Dict) -> str:
    return f"Given the following list of products, classify each product with its category:\nPRODUCTS: {json.dumps(receipt_json)}"

def generate_vision_query(base64_image: str) -> str:
    return f"Take the following base64-encoded image of a receipt and extract the product information:\nIMAGE: {base64_image}"

# Create specialized prompt generators
create_classification_prompt = create_parser_prompt(
    ClassifiedProduct,
    generate_classification_query
)

create_vision_prompt = create_parser_prompt(
    Receipt,
    generate_vision_query
)
