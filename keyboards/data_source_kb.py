from telegram import KeyboardButton, ReplyKeyboardMarkup
from db.functions.receipts import fetch_user_receipts
from db.functions.products import fetch_user_products
from ptb_pagination import InlineKeyboardPaginator
from typing import Union
from .paginator_kb import generic_paginator
from logs.logger import logger

COLUMNS_NUMBER = 1
MAX_PAGE_SIZE = 6

def data_source_kb():
    keyboard = [
        [KeyboardButton("Как добавлять чеки"), KeyboardButton("Список чеков")],
        [KeyboardButton("Список купленных продуктов")],
        [KeyboardButton("Список нераспознанных продуктов")],
        [KeyboardButton("Главное меню")],
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

async def receipts_paginator(update, context, user_id: int, page: int) -> Union[InlineKeyboardPaginator, bool]:
    max_items = len(await fetch_user_receipts(user_id, offset=0, limit=300))
    offset = (page - 1) * MAX_PAGE_SIZE  # Calculate offset for pagination
    receipts = await fetch_user_receipts(user_id, offset=offset, limit=MAX_PAGE_SIZE)

    return await generic_paginator(
        page=page,
        max_page_size=MAX_PAGE_SIZE,
        columns_number=COLUMNS_NUMBER,
        items=receipts,
        text_func=lambda r: f"Время на чеке: {r.time}",
        data_func=lambda r: f"receipt#{r.id}",
        data_pattern='receipts_page#{page}',
        max_items=max_items
    )

async def products_paginator(update, context, user_id: int, page: int) -> Union[InlineKeyboardPaginator, bool]:
    max_items = len(await fetch_user_products(user_id, offset=0, limit=300))
    offset = (page - 1) * MAX_PAGE_SIZE  # Calculate offset for pagination
    products = await fetch_user_products(user_id, offset=offset, limit=MAX_PAGE_SIZE)

    return await generic_paginator(
        page=page,
        max_page_size=MAX_PAGE_SIZE,
        columns_number=COLUMNS_NUMBER,
        items=products,
        text_func=lambda p: (
            f"🛒 {p.name[:26] + '...' if len(p.name) > 26 else p.name} "
            f"- (кол-во: {p.quantity})"
        ),
        data_func=lambda p: f"product#{p.id}",
        data_pattern='products_page#{page}',
        max_items=max_items
    )
