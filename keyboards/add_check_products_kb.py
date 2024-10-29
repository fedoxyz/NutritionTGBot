from telegram import ReplyKeyboardMarkup, InlineKeyboardButton
from ptb_pagination import InlineKeyboardPaginator

from typing import List, Union
import math

COLUMNS_NUMBER = 1  # One product per row
MAX_PAGE_SIZE = 7  # Products per page

def confirm_cancel_kb():
    """Generate a confirmation and cancellation keyboard."""
    return ReplyKeyboardMarkup(
        [["✅ Подтвердить", "❌ Отменить"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

async def products_paginator(products: List[dict], page: int) -> Union[InlineKeyboardPaginator, bool]:
    max_products = len(products)
    if max_products == 0:
        return False

    paginator = InlineKeyboardPaginator(
        math.ceil(max_products / MAX_PAGE_SIZE),
        current_page=page,
        data_pattern='product_page#{page}'  # Custom pattern for pagination callbacks
    )

    # Add product list to the paginator
    product_kb = products_list_kb(products[(page - 1) * MAX_PAGE_SIZE: page * MAX_PAGE_SIZE])
    paginator.add_before(product_kb)


    return paginator


def products_list_kb(products_list: List[dict]) -> List[List[InlineKeyboardButton]]:
    """Generate inline buttons for products."""
    products_kb = []
    for product_chunk in chunks(products_list, COLUMNS_NUMBER):
        sub_keyboard = []
        for i, product in enumerate(product_chunk):
            button_text = f"🛒 {product['name'][:26] + '...' if len(product['name']) > 26 else product['name']} - (кол-во: {product['quantity']})"
            sub_keyboard.append(
                InlineKeyboardButton(button_text, callback_data="donothing"),
            )
        products_kb.append(sub_keyboard)
    return products_kb


def chunks(lst, n):
    """Yield successive n-sized chunks from the list."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

