from typing import Callable, List, Any, Union, Generator
from telegram import InlineKeyboardButton
from ptb_pagination import InlineKeyboardPaginator
import math
from logs.logger import logger

async def generic_paginator(
    page: int,
    items: List[Any],  # Pass the list of items directly
    text_func: Callable[[Any], str],
    data_func: Callable[[Any], str],
    data_pattern: str,
    max_page_size: int = 5,  # Default argument
    columns_number: int = 2, # Default argument
    max_items: int = -1
) -> Union[InlineKeyboardPaginator, bool]:
    """Creates a paginator with provided items and generated buttons."""
    
    max_items = len(items) if max_items == -1 else max_items  # Get the length of the passed items
    if max_items == 0:
        return False

    total_pages = math.ceil(max_items / max_page_size)
    paginator = InlineKeyboardPaginator(
        total_pages,
        current_page=page,
        data_pattern=data_pattern
    )

    # Calculate the offset based on the current page
    offset = (page - 1) * max_page_size
   
    items_for_page = items[offset:offset + max_page_size] if max_items == len(items) else items  
    # Generate keyboard with fetched items
    item_list_kb = generate_keyboard(items_for_page, columns_number, text_func, data_func)
    paginator.add_before(item_list_kb)

    return paginator

def generate_keyboard(
    items: List[Any], 
    columns: int, 
    text_func: Callable[[Any], str], 
    data_func: Callable[[Any], str]
) -> List[List[InlineKeyboardButton]]:
    """
    Generate a keyboard layout for a list of items.

    Args:
        items: List of elements to display.
        columns: Number of columns for the keyboard layout.
        text_func: Function to generate button text from an item.
        data_func: Function to generate callback data from an item.

    Returns:
        List of InlineKeyboardButton rows.
    """
    return [
        [
            InlineKeyboardButton(
                text=text_func(item), 
                callback_data=data_func(item)
            ) for item in item_chunk
        ]
        for item_chunk in chunks(items, columns)
    ]

def chunks(lst: List[Any], n: int) -> Generator[List[Any], None, None]:
    """Yield successive n-sized chunks from the list."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
