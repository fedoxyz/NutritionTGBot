from logger import logger
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from typing import Dict, Callable, Awaitable
from utils.json_utils import parse_json_file
from .receipt_overview_handler import products_list_pag_callback
from utils.message_utils import delete_message_by_id
from grpc_client import GRPCClient
import json

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]


async def handle_json_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the message contains a document
    if not update.message or not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл чека.")
        return
    
    await delete_message_by_id(update, context, 'receipt_message_id')

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
    
    products = json.dumps(data["products"], ensure_ascii=False)
    await classify_test(products)

    await products_list_pag_callback(update, context)

async def classify_test(products):
    grpc_client = GRPCClient()

    logger.debug(f"products - {products}")

    """Process the photo and return the data."""
    response = await grpc_client.classify_products(products)

    logger.debug(f"{json.loads(response.data)}")



def setup_json_receipt_handlers(application):
    application.add_handler(MessageHandler(
        filters.Document.FileExtension("json") & ~filters.COMMAND,
        handle_json_receipt
    ))

    logger.debug("Добавлены receipt process handlers")



