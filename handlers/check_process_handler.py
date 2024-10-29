from keyboards.main_kb import main_kb
from keyboards.add_check_products_kb import confirm_cancel_kb, products_paginator 
from logs.logger import logger
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message, edit_message
from utils.chat_filters import private_chat_only
from utils.json_utils import parse_json_file, validate_check_data
from db.functions.checks import new_check

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

# Store user-specific temporary data (e.g., parsed products)
user_checks = {}

async def handle_json_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the message contains a document
    if not update.message or not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл чека.")
        return

    # Download the file as a bytearray
    file = await update.message.document.get_file()
    file_content = await file.download_as_bytearray()

    # Parse the JSON file into a dictionary
    data = parse_json_file(file_content)  # This now returns {"check_date": ..., "products": ...}
    
    if not data or 'products' not in data or not data['products']:
        await update.message.reply_text("Не удалось распознать чек или продукты отсутствуют.")
        return

    # Store the parsed products temporarily for the user
    user_checks[update.effective_user.id] = {"products": data['products'], "check_date": data['check_date']}

    # Create a text variable to summarize the check details
    text = f"Чек на дату: {data['check_date']}\n\nПродукты:\n"

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
    
    check_data = user_checks.get(user_id)
    products = check_data['products']

    page = int(query.data.split('#')[1])
    paginator = await products_paginator(products, page)
    text = f"Чек на дату: {check_data['check_date']}\n\nПродукты:\n"
    text += f"Страница {page}"

    await edit_message(query, text=text, reply_markup=paginator.markup)


async def confirm_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    check_data = user_checks.pop(user_id, None)  # Retrieve and remove the temporary data

    if check_data:
        # Simulate adding the check to the database
        success = await new_check(user_id, check_data)
        text = "Чек успешно добавлен." if success else "Ошибка при добавлении чека."
    else:
        text = "Нет данных для добавления."

    await update.message.reply_text(text, reply_markup=main_kb())

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_checks.pop(user_id, None)  # Discard the temporary data

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

def setup_check_process_handlers(application):
    check_process_filter = filters.Regex('^(' + '|'.join(map(re.escape, menu_options.keys())) + ')$')
    application.add_handler(MessageHandler(check_process_filter & ~filters.COMMAND, handler))
    application.add_handler(MessageHandler(
        filters.Document.FileExtension("json") & ~filters.COMMAND,
        handle_json_check
    ))
    application.add_handler(CallbackQueryHandler(product_pag_callback, pattern=r"^product_page#\d+$"))

    logger.debug("Добавлены check process handlers")



