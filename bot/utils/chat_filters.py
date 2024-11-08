from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType

from logger import logger

def is_private_chat(update: Update) -> bool:
    return update.effective_chat.type == ChatType.PRIVATE

def private_chat_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not is_private_chat(update):
            return
        return await func(update, context)
    return wrapper

def custom_channel_only(custom_channel_id):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            logger.debug(f"ID кастомного канала: {custom_channel_id}")
            logger.debug(f"update.effective_chat.id: {update.effective_chat.id}")
            if update.effective_chat.id != int(custom_channel_id):
                logger.debug("update.effective_chat.id не совпадает с custom_channel_id");
                return
            return await func(update, context)
        return wrapper
    return decorator
