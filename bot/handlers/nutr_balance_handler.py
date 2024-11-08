from keyboards.main_kb import main_kb
from logger import logger
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message
from utils.chat_filters import private_chat_only

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def nutr_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Посчитать баланс макронутриентов"
    reply_markup = main_kb()
    await send_message(update, context, text, reply_markup=reply_markup) 

menu_options: Dict[str, OptionHandler] = {
    "Баланс макронутриентов": nutr_balance,
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

def setup_nutr_balance_handlers(application):
    nutr_balance_filter = filters.Regex('^(' + '|'.join(map(re.escape, menu_options.keys())) + ')$')
    application.add_handler(MessageHandler(nutr_balance_filter & ~filters.COMMAND, handler))
    logger.debug("Добавлены nutr balance handlers")



