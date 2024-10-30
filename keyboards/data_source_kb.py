from telegram import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from db.functions.receipts import fetch_user_receipts
from ptb_pagination import InlineKeyboardPaginator
import math
from typing import Union

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

async def receipts_paginator(user_id: int, page: int)  -> Union[InlineKeyboardPaginator, bool]:
    max_receipts = len(await fetch_user_receipts(user_id, offset=0, limit=300))
    if (max_receipts == 0):
        return False

    paginator = InlineKeyboardPaginator(
        math.ceil(max_receipts / MAX_PAGE_SIZE),
        current_page=page,
        data_pattern='receipts_page#{page}'
    )
    logger.debug(f"Page is {page}")
    receipt_list_kb = receipts_list_kb(
        await fetch_user_receipts(
            user_id,
            offset=(page - 1) * MAX_PAGE_SIZE,
            limit=MAX_PAGE_SIZE
        )
    )
    paginator.add_before(receipt_list_kb)

    return paginator


def receipts_list_kb(receipts_list: list) -> list:
    receipt_history_kb = []
    for receipt_sub_list in chunks(receipts_list, COLUMNS_NUMBER):
        sub_keyboard = []
        for receipt in receipt_sub_list:
            logger.debug(f"receipt in receipt_sub_list - {receipt}")
            button_text = f"Время на чеке: {receipt.time}"
            sub_keyboard.append(
                InlineKeyboardButton(
                    button_text, callback_data=receipt.id
                )
            )
        receipt_history_kb.append(sub_keyboard)
    return receipt_history_kb

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

