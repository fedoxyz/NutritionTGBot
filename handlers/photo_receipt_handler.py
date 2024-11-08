from logs.logger import logger
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from typing import Callable, Awaitable
from .receipt_overview_handler import products_list_pag_callback
from utils.message_utils import delete_message_by_id
#from ai.main import process_receipt
from utils.photo_utils import qr_process_receipt

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def handle_photo_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.photo:
        await update.message.reply_text("Пожалуйста, отправьте фотографию чека.")
        return

    await delete_message_by_id(update, context, 'receipt_message_id')

    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    photo_bytes = await photo_file.download_as_bytearray()

    # Try processing with QR code first
    data = qr_process_receipt(photo_bytes)
    if not data:
        # Fallback to AI processing if QR code processing fails
        data = 1 # process_receipt(photo_bytes)

    if not data or 'products' not in data or not data['products']:
        await update.message.reply_text("Не удалось распознать чек или продукты отсутствуют.")
        return

    context.user_data['current_receipt'] = {
        'products': [product.dict() for product in data['products']],
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

