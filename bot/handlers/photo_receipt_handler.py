from logger import logger
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from typing import Callable, Awaitable
from .receipt_overview_handler import products_list_pag_callback
from utils.message_utils import delete_message_by_id, send_message
from utils.photo_utils import qr_process_receipt
from grpc_client import GRPCClient
import json
from datetime import datetime
from utils.state_manager import get_current_state, set_current_state

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

grpc_client = GRPCClient()

async def handle_photo_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.photo:
        await send_message(update, context, "Пожалуйста, отправьте фотографию чека.")
        return

    current_state = get_current_state(context)
    if current_state == "PHOTO_PROCESSING":
        await send_message(update, context, "Ваше фото уже в очереди, пожалуйста подождите или попробуйте позже.")
        return

    await delete_message_by_id(update, context, 'receipt_message_id')

    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    photo_bytes = bytes(await photo_file.download_as_bytearray())

    await send_message(update, context, text="Ваша фотография обрабатывается, пожалуйста подождите.")
    set_current_state(context, "PHOTO_PROCESSING")

    # Process the photo
    data = await process_photo(photo_bytes, context)

    if not data or 'products' not in data or not data['products']:
        set_current_state(context, "PHOTO_PROCESSED")
        await send_message(update, context, "Не удалось распознать чек или продукты отсутствуют.")
        return

    # Append 'id' to each product
    products_with_ids = [
        {**product, 'id': index + 1} for index, product in enumerate(data['products'])
    ]
    receipt_date = datetime.strptime(data["date"], "%d-%m-%y %H:%M")
    context.user_data['current_receipt'] = {
        'products': products_with_ids,
        'receipt_date': receipt_date,
        'current_page': 1,
        'editing_mode': False,
        'selected_product': None
    }
    set_current_state(context, "PHOTO_PROCESSED")

    await products_list_pag_callback(update, context)
    return

async def process_photo(photo_bytes, context):
    """Process the photo and return the data."""
    # Try processing with QR code first
    data = qr_process_receipt(photo_bytes)
    if not data:
        response = await grpc_client.process_receipt(photo_bytes)
        if response.success:
            data = json.loads(response.data)
        else:
            await send_message(context, "Возникла ошибка при обработке фотографии. Попробуйте снова.")
            set_current_state(context, "ERROR")
            return None
    return data

# Setup the photo receipt handlers in the application
def setup_photo_receipt_handlers(application):
    application.add_handler(MessageHandler(
        filters.PHOTO & ~filters.COMMAND,  # Handler for photo messages excluding commands
        handle_photo_receipt
    ))

    logger.debug("Добавлены обработчики для обработки фотографий чеков")

