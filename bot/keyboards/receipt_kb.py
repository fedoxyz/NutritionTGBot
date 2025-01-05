from telegram import ReplyKeyboardMarkup
from ptb_pagination import InlineKeyboardPaginator
from typing import List, Union
from .paginator_kb import generic_paginator  # Assuming this is where it's defined

COLUMNS_NUMBER = 1  # One product per row
MAX_PAGE_SIZE = 7  # Products per page

def confirm_cancel_kb():
    """Generate a confirmation and cancellation keyboard."""
    return ReplyKeyboardMarkup(
        [["✅ Подтвердить", "❌ Отменить"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

async def products_paginator(update, context, user_id, page: int, **kwargs) -> Union[InlineKeyboardPaginator, bool]:
    """Generate a paginated view for the products."""
    products = context.user_data["current_receipt"]["products"]
    return await generic_paginator(
        page=page,
        items=products, 
        text_func=lambda p: (
            f"🛒 {p['name'][:26] + '...' if len(p['name']) > 26 else p['name']} "
            f"- (кол-во: {p['quantity']})"
        ),
        data_func=lambda p: f"product#{p['id']}",  
        data_pattern='product_page#{page}',
        max_page_size=MAX_PAGE_SIZE,
        columns_number=COLUMNS_NUMBER,
        **kwargs
    )
