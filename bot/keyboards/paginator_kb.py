from typing import Callable, List, Any, Union, Generator
from telegram import InlineKeyboardButton
from ptb_pagination import InlineKeyboardPaginator
import math
from logger import logger
from telegram import Update
from telegram.ext import ContextTypes
from utils.message_utils import send_message, edit_message

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

    logger.debug(f"{page} page inside generic_paginator")
    total_pages = math.ceil(max_items / max_page_size)
    page = page - 1 if total_pages < page else page
    paginator = InlineKeyboardPaginator(
        total_pages,
        current_page=page,
        data_pattern=data_pattern
    )

    # Calculate the offset based on the current page
    offset = (page - 1) * max_page_size
    logger.debug(f"{items} - items inside generic_paginator")
    logger.debug(f"{offset} - offset inside generic_paginator")
    logger.debug(f"{max_page_size} - max_page_size inside generic_paginator")
    logger.debug(f"{max_items == len(items)}")
    items_for_page = items[offset:offset + max_page_size] if max_items == len(items) else items  
    # Generate keyboard with fetched items
    logger.debug(f"{items_for_page} - items_for_page inside generic_paginator")
    logger.debug(f"{columns_number} - columns_number inside generic_paginator")
    logger.debug(f"{text_func} - text_func inside generic_paginator")
    logger.debug(f"{data_func} - data_func inside generic_paginator")
    item_list_kb = generate_keyboard(items_for_page, columns_number, text_func, data_func)
    paginator.add_before(item_list_kb)

    return paginator, page

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


async def handle_pagination(update: Update, context: ContextTypes.DEFAULT_TYPE, paginator_func, list_text: str, page = None, **kwargs) -> None:
    query = update.callback_query
    if query:
        await query.answer()
        logger.debug(f"query.data: {query.data}")
    user_id = update.effective_user.id
    logger.debug(f"{page}")
    page = query.data.split('#')[1] if query and query.data and page == None else page if query and query.data and page != None else 1
    logger.debug(f"{page} - page inside handle_pagination")
    paginator, current_page = await paginator_func(update, context, user_id, int(page), **kwargs)
    text = f"{list_text}\nСтраница {current_page}"
    
    if query:
        return await edit_message(query, text=text, reply_markup=paginator.markup)
    else:
        return await send_message(update, context, text=text, reply_markup=paginator.markup)

async def handle_list_display(update: Update, context: ContextTypes.DEFAULT_TYPE, paginator_func, list_text: str) -> None:
    text = list_text
    user_id = update.effective_user.id
    paginator, current_page = await paginator_func(update, context, user_id, 1)
    if paginator:
        text += f"\nСтраница {current_page}"
        return await send_message(update, context, text, reply_markup=paginator.markup)
    else:
        text += "\nПусто"
        return await send_message(update, context, text)
