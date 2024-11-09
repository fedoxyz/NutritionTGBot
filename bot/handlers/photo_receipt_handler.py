from logger import logger
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from typing import Callable, Awaitable
from .receipt_overview_handler import products_list_pag_callback
from utils.message_utils import delete_message_by_id
from utils.photo_utils import qr_process_receipt
from grpc_client import GRPCClient
import json

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

grpc_client = GRPCClient()

async def handle_photo_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.photo:
        await update.message.reply_text("Пожалуйста, отправьте фотографию чека.")
        return

    await delete_message_by_id(update, context, 'receipt_message_id')

    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    photo_bytes = bytes(await photo_file.download_as_bytearray())

    # Try processing with QR code first
    data = qr_process_receipt(photo_bytes)
    if not data:
        response = grpc_client.process_receipt(photo_bytes)
        if response.success:
            data = json.loads(response.data)
        else:
            await update.message.reply_text(f"Error processing receipt: {response.error}")
            return
    
    if not data or 'products' not in data or not data['products']:
        await update.message.reply_text("Не удалось распознать чек или продукты отсутствуют.")
        return
    
    # Append 'id' to each product
    products_with_ids = [
        {**product, 'id': index + 1} for index, product in enumerate(data['products'])
    ]
    
    context.user_data['current_receipt'] = {
        'products': products_with_ids,
        'receipt_date': data['date'],
        'current_page': 1,
        'editing_mode': False,
        'selected_product': None
    }

    await products_list_pag_callback(update, context)

# Setup the photo receipt handlers in the application
def setup_photo_receipt_handlers(application):
    application.add_handler(MessageHandler(
        filters.PHOTO & ~filters.COMMAND,  # Handler for photo messages excluding commands
        handle_photo_receipt
    ))

    logger.debug("Добавлены обработчики для обработки фотографий чеков")

