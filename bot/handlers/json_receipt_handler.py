from logger import logger
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from typing import Dict, Callable, Awaitable
from utils.json_utils import parse_json_file
from .receipt_overview_handler import products_list_pag_callback
from utils.message_utils import delete_message_by_id
from grpc_client import GRPCClient
import json
import re

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]


async def handle_json_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the message contains a document
    if not update.message or not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл чека.")
        return
    
    await delete_message_by_id(update, context, 'receipt_message_id')
    await delete_message_by_id(update, context, 'product_message_id')


    # Download the file as a bytearray
    file = await update.message.document.get_file()
    file_content = await file.download_as_bytearray()

    # Parse the JSON file into a dictionary
    data = parse_json_file(file_content)  # This now returns {"receipt_date": ..., "products": ...}
    
    if not data or 'products' not in data or not data['products']:
        await update.message.reply_text("Не удалось распознать чек или продукты отсутствуют.")
        return

    clean_string = lambda x: re.sub(r'[^а-яА-ЯёЁa-zA-Z\s]', ' ', x).lower().strip()
    no_spaces = lambda x: re.sub(r'\s+', ' ', x)
   
    product_names = [
    no_spaces(clean_string(product["name"]))
    for product in data["products"]
    ]

    # Without preprocessing
    #product_names = [product["name"] for product in data["products"]]

    categories = await classify_products(product_names)

    if categories:
        classified_products = [
        {**product, "category": category}
        for product, category in zip(data["products"], categories)
        ]

        logger.debug(f"classfied products - {classified_products}")

        context.user_data['current_receipt'] = {
                'products': classified_products,
                'receipt_date': data["receipt_date"],
                'current_page': 1,
                'editing_mode': False,
                'selected_product': None,
                'new_receipt': True
            }

        await products_list_pag_callback(update, context)
    else:
        await update.message.reply_text("При классификации продуктов произошла ошибка. Повторите позже.")


async def classify_products(product_names):
    grpc_client = GRPCClient()

    logger.debug(f"product names - {product_names}")

    response = await grpc_client.classify_products(json.dumps(product_names, ensure_ascii=False))

    logger.debug(f"{response.data}")
    if response.success:
        return json.loads(response.data)
    else:
        return False



def setup_json_receipt_handlers(application):
    application.add_handler(MessageHandler(
        filters.Document.FileExtension("json") & ~filters.COMMAND,
        handle_json_receipt
    ))

    logger.debug("Добавлены receipt process handlers")



