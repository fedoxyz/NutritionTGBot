from keyboards.main_kb import main_kb
from keyboards.json_receipt_kb import confirm_cancel_kb, products_paginator 
from logs.logger import logger
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message, edit_message
from utils.chat_filters import private_chat_only
from utils.json_utils import parse_json_file, validate_receipt_data
from db.functions.receipts import new_receipt

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

# Store user-specific temporary data (e.g., parsed products)
user_receipts = {}

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

    # Store the parsed products temporarily for the user
    user_receipts[update.effective_user.id] = {"products": data['products'], "receipt_date": data['receipt_date']}

    # Create a text variable to summarize the receipt details
    text = f"Чек на дату: {data['receipt_date']}\n\nПродукты:\n"

    # Show the first page of products using pagination
    paginator = await products_paginator(data['products'], page=1)
    logger.debug(paginator.markup)
    # Send the summarized text and pagination buttons
    if paginator:
        await send_message(update, context, text=text, reply_markup=paginator.markup, parse_mode=None)
    else:
        await send_message(update, context, text=text)  # If no pagination needed

    # Send confirmation/cancel options to the user
    await send_message(update, context, text="Выберите действие:", reply_markup=confirm_cancel_kb()) 

async def product_pag_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    query = update.callback_query
    await query.answer()
    

    logger.debug(f"query.data of product_pag_callback: {query.data}")
    
    receipt_data = user_receipts.get(user_id)
    products = receipt_data['products']

    page = int(query.data.split('#')[1])
    paginator = await products_paginator(products, page)
    text = f"Чек на дату: {receipt_data['receipt_date']}\n\nПродукты:\n"
    text += f"Страница {page}"

    await edit_message(query, text=text, reply_markup=paginator.markup)


async def confirm_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    receipt_data = user_receipts.pop(user_id, None)  # Retrieve and remove the temporary data

    if receipt_data:
        # Simulate adding the receipt to the database
        success = await new_receipt(user_id, receipt_data)
        text = "Чек успешно добавлен." if success else "Ошибка при добавлении чека."
    else:
        text = "Нет данных для добавления."

    await update.message.reply_text(text, reply_markup=main_kb())

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_receipts.pop(user_id, None)  # Discard the temporary data

    await update.message.reply_text(
        "Добавление чека отменено.",
        reply_markup=main_kb(),
    )
menu_options: Dict[str, OptionHandler] = {
        "✅ Подтвердить": confirm_add,
        "❌ Отменить": cancel
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

def setup_receipt_process_handlers(application):
    receipt_process_filter = filters.Regex('^(' + '|'.join(map(re.escape, menu_options.keys())) + ')$')
    application.add_handler(MessageHandler(receipt_process_filter & ~filters.COMMAND, handler))
    application.add_handler(MessageHandler(
        filters.Document.FileExtension("json") & ~filters.COMMAND,
        handle_json_receipt
    ))
    application.add_handler(CallbackQueryHandler(product_pag_callback, pattern=r"^product_page#\d+$"))

    logger.debug("Добавлены receipt process handlers")



