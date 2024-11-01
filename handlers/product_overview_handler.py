from keyboards.main_kb import main_kb
from logs.logger import logger
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message, edit_message, delete_message_by_id
from utils.chat_filters import private_chat_only
from db.functions.receipts import new_receipt
from keyboards.paginator_kb import handle_pagination
from keyboards.product_overview_kb import product_overview_kb, confirm_cancel_kb
from .receipt_overview_handler import products_list_pag_callback

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def product_overview_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = context.user_data["current_receipt"]
    query = update.callback_query
    await query.answer()

    # Retrieve the selected product ID and product details
    selected_product_id = int(query.data.split('#')[1])
    selected_product = next((p for p in data["products"] if p["id"] == selected_product_id), None)
    
    # Update context with selected product
    if selected_product:
        context.user_data['current_receipt']['selected_product'] = selected_product

        # Text for product details
        text = f"Название продукта: {selected_product['name']}\n"
        text += f"Количество: {selected_product['quantity']}"
        
        await delete_message_by_id(update, context, 'product_message_id')

        # Send message with inline keyboard
        product_message = await query.message.reply_text(
            text=text,
            reply_markup=product_overview_kb(selected_product_id)
        )
        context.user_data['product_message_id'] = product_message.id
        await query.message.reply_text(text="Выберите опцию", reply_markup=confirm_cancel_kb()) 
    else:
        await query.edit_message_text("Продукт не найден.")

async def confirm_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    
    context.user_data["current_receipt"] = {
        "selected_product": None,
        }

    await delete_message_by_id(update, context, 'product_message_id')


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['current_receipt'].pop('selected_product', None)

    await delete_message_by_id(update, context, 'product_message_id')

    await update.message.reply_text(
        "Назад к списку продуктов.",
    )
    await products_list_pag_callback(update, context)

menu_options: Dict[str, OptionHandler] = {
        "✅ Подтвердить": confirm_add,
        "🔙 Назад": back
        }

# Handlers for each action
async def edit_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Handle name editing
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Введите новое название продукта:")

async def edit_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Handle quantity editing
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Введите новое количество продукта:")

async def remove_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Handle product removal
    await update.callback_query.answer()
    # Example: remove from list and update context
    product_id = int(update.callback_query.data.split('#')[1])
    context.user_data['current_receipt']['products'] = [
        p for p in context.user_data['current_receipt']['products'] if p["id"] != product_id
    ]
    await update.callback_query.edit_message_text("Продукт удален из списка.")
    context.user_data["current_receipt"]["selected_product"] = None
    await products_list_pag_callback(update, context)



@private_chat_only
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        logger.warning("Получен update без сообщения или текста в handler")
        return

    option = update.message.text
    handler = menu_options.get(option)
    
    if handler:
        await handler(update, context)
    else:
        await update.message.reply_text(f"Неизвестная опция: {option}")

def setup_product_overview_handlers(application):
    receipt_process_filter = filters.Regex('^(' + '|'.join(map(re.escape, menu_options.keys())) + ')$')
    application.add_handler(MessageHandler(receipt_process_filter & ~filters.COMMAND, handler))
    application.add_handler(CallbackQueryHandler(product_overview_callback, pattern=r"^product#\d+$"))
    application.add_handler(CallbackQueryHandler(edit_name, pattern=r"^edit_name#\d+$"))
    application.add_handler(CallbackQueryHandler(edit_quantity, pattern=r"^edit_quantity#\d+$"))
    application.add_handler(CallbackQueryHandler(remove_product, pattern=r"^remove_product#\d+$"))

    logger.debug("Добавлены product overview handlers")



