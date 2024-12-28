from keyboards.main_kb import main_kb
from keyboards.receipt_kb import confirm_cancel_kb, products_paginator 
from logger import logger
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from typing import Dict, Callable, Awaitable
from utils.message_utils import delete_message_by_id, send_message, edit_message, delete_message_by_id
from utils.chat_filters import private_chat_only
from db.functions.receipts import new_receipt
from keyboards.paginator_kb import handle_pagination

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def products_list_pag_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    is_product_page_callback = False

    receipt_data = context.user_data["current_receipt"]

    text = f"Чек на дату: {receipt_data['receipt_date']}\n\nКатегории: {[product['category'] for product in receipt_data['products']]}\n"

    max_items = len(receipt_data["products"])

    logger.debug(f"{max_items} - max items")
    if max_items < 1:
        await cancel(update, context)
        return

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        callback_data = query.data.split('#')
        logger.debug(f"{callback_data} - callback_data inside products list pag callback")
        logger.debug(f'{context.user_data["current_receipt"]["current_page"]} - current_page in user_data')
        if 'product_page' in callback_data[0]:
            page = callback_data[1]
            is_product_page_callback = True
        else:
            page = context.user_data["current_receipt"]["current_page"]
    else:
        page = 1
    logger.debug(f"page before handle_pagination {page}")
    message = await handle_pagination(update, context, products_paginator, text, max_items=max_items, page=page)
    context.user_data['receipt_message_id'] = message.message_id
    context.user_data["current_receipt"]["current_page"] = page
    logger.debug(f"{is_product_page_callback} - is product page callback")
    if is_product_page_callback:
        return
    else:
        await send_message(update, context, text="\nВыберите опцию", reply_markup=confirm_cancel_kb())

async def select_receipt_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return
#    if update.callback_query:
#        query = update.callback_query
#        await query.answer()
#        callback_data = query.data.split('#')
#        if 'receipt' in callback_data[0]:
    #        receipt_data = fetch_user_receipt()
    #        context.user_data["current_receipt"] = 

async def confirm_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    receipt_data = context.user_data["current_receipt"]  # Retrieve and remove the temporary data

    if receipt_data:
        # Simulate adding the receipt to the database
        success = await new_receipt(user_id, receipt_data)
        text = "Чек успешно добавлен." if success else "Ошибка при добавлении чека. Попробуйте снова."
    else:
        text = "Нет данных для добавления."

    await delete_message_by_id(update, context, "receipt_message_id")

    await send_message(update, context, text=text, reply_markup=main_kb())

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop('current_receipt', None)

    await delete_message_by_id(update, context, "receipt_message_id")

    await send_message(
            update,
            context,
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
    application.add_handler(CallbackQueryHandler(products_list_pag_callback, pattern=r"^product_page#\d+$"))

    logger.debug("Добавлены receipt process handlers")



