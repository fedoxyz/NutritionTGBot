from keyboards.receipt_kb import confirm_cancel_kb 
from logs.logger import logger
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from typing import Dict, Callable, Awaitable
from utils.json_utils import parse_json_file
from .receipt_overview_handler import product_pag_callback

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def handle_json_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the message contains a document
    if not update.message or not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл чека.")
        return

    # Download the file as a bytearray
    file = await update.message.document.get_file()
    file_content = await file.download_as_bytearray()

    # Parse the JSON file into a dictionary
    data = parse_json_file(file_content)  # This now returns {"receipt_date": ..., "products": ...}
    
    if not data or 'products' not in data or not data['products']:
        await update.message.reply_text("Не удалось распознать чек или продукты отсутствуют.")
        return
    
    context.user_data['current_receipt'] = {
            'products': data["products"],
            'receipt_date': data["receipt_date"],
            'current_page': 1,
            'editing_mode': False,
            'selected_product': None
        }

    await product_pag_callback(update, context)


def setup_json_receipt_handlers(application):
    application.add_handler(MessageHandler(
        filters.Document.FileExtension("json") & ~filters.COMMAND,
        handle_json_receipt
    ))

    logger.debug("Добавлены receipt process handlers")



