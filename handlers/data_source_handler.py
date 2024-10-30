from logs.logger import logger
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message, edit_message
from utils.chat_filters import private_chat_only
from keyboards.data_source_kb import receipts_paginator, data_source_kb

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def receipts_list_pag_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query:
        await query.answer()
        logger.debug(f"query.data of receipt_pag_callback: {query.data}")
    user_id = update.effective_user.id
    page = int(query.data.split('#')[1]) if query and query.data else 1
    paginator = await receipts_paginator(user_id, page)
    text = f"Список чеков:\n"
    text += f"Страница {page}"
    
    if query:
        await edit_message(query, text=text, reply_markup=paginator.markup)
    else:
        await send_message(update, context, text=text, reply_markup=paginator.markup)

async def data_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Выберите опцию: "
    await send_message(update, context, text, reply_markup=data_source_kb()) 

async def how_to_receipts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Как добавлять чеки"
    await send_message(update, context, text, reply_markup=data_source_kb())

async def receipts_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Список чеков:"
    user_id = update.effective_user.id
    paginator = await receipts_paginator(user_id, 1)
    if paginator:
        text += "\nСтраница 1"
        await send_message(update, context, text, reply_markup=paginator.markup)
    else:
        text += "\nПусто"
        await send_message(update, context, text)

async def purchased_p_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Список купленных продуктов"
    await send_message(update, context, text, reply_markup=data_source_kb())

async def unrecognized_p_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Список нераспознанных продуктов"
    await send_message(update, context, text, reply_markup=data_source_kb())

menu_options: Dict[str, OptionHandler] = {
    "Источники данных": data_source,
    "Как добавлять чеки": how_to_receipts,
    "Список чеков": receipts_list,
    "Список купленных продуктов": purchased_p_list,
    "Список нераспознанных продуктов": unrecognized_p_list,
}

@private_chat_only
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        logger.warning("Получен update без сообщения или текста в handler")
        return

    option = update.message.text
    handler = menu_options.get(option)
    
    if handler:
        await handler(update, context)
    else:
        await update.message.reply_text(f"Неизвестная опция: {option}")

def setup_data_source_handlers(application):
    filter = filters.Regex('^(' + '|'.join(map(re.escape, menu_options.keys())) + ')$')
    application.add_handler(MessageHandler(filter & ~filters.COMMAND, handler))
    application.add_handler(CallbackQueryHandler(receipts_list_pag_callback, pattern=r"^receipts_page#\d+$"))

    logger.debug("Добавлены menu handlers")


