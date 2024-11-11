import json
import base64
from typing import Dict, Callable, TypeVar, Type, Any, Tuple, List
from pydantic import BaseModel
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic_schemas import Receipt, ClassifiedProduct

T = TypeVar('T', bound=BaseModel)

def create_parser_prompt(
    pydantic_model: Type[T],
    system_prompt: str,
    query_generator: Callable[[Any], Tuple[Tuple[str, List[Any]], Dict[str, str]]],
) -> Callable[[Any], ChatPromptTemplate]:
    """
    Create a universal prompt generator function using ChatPromptTemplate,
    supporting both text and image inputs with a customizable system prompt.
    """
    parser = JsonOutputParser(pydantic_object=pydantic_model)
    format_instructions = parser.get_format_instructions()
    
    def generate_prompt(input_data: Any) -> ChatPromptTemplate:
        # Handle image data and encode as base64
        user_query, invoke_data = query_generator(input_data)
        prompt = ChatPromptTemplate(
            [
                ("system", system_prompt),
                user_query
            ], 
            partial_variables={"format_instructions": format_instructions},
        )
        print(prompt)
        return prompt.invoke(invoke_data)

    return generate_prompt

def generate_vision_query(input_data: bytes) -> Tuple[Tuple[str, List[Dict[str, str]]], Dict[str, str]]:
    image_data = base64.b64encode(input_data).decode("utf-8")
    query = (
             "user", 
                [
                    {
                        "type": "image_url", 
                            "image_url": {"url": "data:image/jpeg;base64,{image_data}"}
                    }
                ]
            )
    data = {
            "image_data": image_data
            }
    return query, data 

def generate_classification_query(receipt_json: Dict) -> Tuple[Tuple[str, List[str]], Dict[str, str]]:
    query_data = f"Given the following list of products, classify each product with its category:\nPRODUCTS: {json.dumps(receipt_json)}"
    query = (
            "user",
                [
                    "{query_data}"
                ],
            )
    data = {
            "query_data": query_data
            }

    return query, data


# Create specialized prompt generators
create_classification_prompt = create_parser_prompt(
    ClassifiedProduct,
    system_prompt="You are a classificator of products in user's receipts. Please classify the given entries from receipt with precisely correct products' and categories' classes. Output information purely and solely in JSON format. {format_instructions}",
    query_generator=generate_classification_query,
)

create_vision_prompt = create_parser_prompt(
    Receipt,
    system_prompt="You are a vision assistant for extracting bought products from user's receipt photo and parse this information. Please provide the date and time in the following format: DD-MM-YYYY HH:MM. Only return the datetime in this format, without seconds, milliseconds, or timezone information. Output information purely and solely in JSON format and be as precise as you can with product names. {format_instructions}",
    query_generator=generate_vision_query,
)
