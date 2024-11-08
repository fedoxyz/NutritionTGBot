from logger import logger
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message
from utils.chat_filters import private_chat_only
from keyboards.main_kb import main_kb

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def product_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Pie chart категорий продуктов"
    await send_message(update, context, text, reply_markup=main_kb()) 

async def ration_diversity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Таблица разнообразия продуктов"
    await send_message(update, context, text, reply_markup=main_kb())

async def products_processed_ratio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Pie chart доли переработанных продуктов"
    await send_message(update, context, text, reply_markup=main_kb())

menu_options: Dict[str, OptionHandler] = {
    "Категории продуктов": product_categories,
    "Разнообразие рациона": ration_diversity,
    "Доля переработанных продуктов": products_processed_ratio,
}

@private_chat_only
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        logger.warning("Получен update без сообщения или текста в menu_handler")
        return

    option = update.message.text
    handler = menu_options.get(option)
    
    if handler:
        await handler(update, context)
    else:
        await update.message.reply_text(f"Неизвестная опция: {option}")

def setup_menu_handlers(application):
    filter = filters.Regex('^(' + '|'.join(map(re.escape, menu_options.keys())) + ')$')
    application.add_handler(MessageHandler(filter & ~filters.COMMAND, handler))
    logger.debug("Добавлены menu handlers")


