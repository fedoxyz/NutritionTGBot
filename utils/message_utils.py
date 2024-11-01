from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from logs.logger import logger

async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None, parse_mode="Markdown", **kwargs):
    # Check for update type and send a reply accordingly
    if update.message:
        return await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode, **kwargs)
    elif update.callback_query:
        return await update.callback_query.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode, **kwargs)

async def edit_message(query, text: str, reply_markup=None, parse_mode="Markdown", **kwargs):
    return await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=parse_mode, **kwargs)

async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, photo, caption: str = None, reply_markup=None, **kwargs):
    return await update.message.reply_photo(photo, caption=caption, reply_markup=reply_markup, parse_mode=ParseMode.HTML, **kwargs)

async def send_photo_group(update: Update, context: ContextTypes.DEFAULT_TYPE, photos, caption: str = None, **kwargs):
    media = [InputMediaPhoto(photo, caption=(caption if i == 0 else None)) for i, photo in enumerate(photos)]
    return await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media, **kwargs)

async def delete_message_by_id(update: Update, context: ContextTypes.DEFAULT_TYPE, message_key: str) -> None:
    """Helper function to delete a message by stored message ID."""
    if message_key in context.user_data:
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=context.user_data[message_key]
            )
        except Exception as e:
            logger.error(f"Error deleting message: {e}")
        finally:
            del context.user_data[message_key]

