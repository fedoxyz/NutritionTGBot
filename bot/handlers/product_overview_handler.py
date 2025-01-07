from db.functions.products import remove_product, update_product_category
from keyboards.product_overview_kb import categories_kb
from logger import logger
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message, delete_message_by_id
from utils.chat_filters import private_chat_only
from keyboards.product_overview_kb import product_overview_kb, confirm_cancel_kb
from .receipt_overview_handler import products_list_pag_callback
import json
from grpc_client import GRPCClient
import urllib.parse

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def product_overview_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    await delete_message_by_id(update, context, "receipt_message_id")

    # Retrieve the selected product ID and product details
    selected_product_id = int(query.data.split('#')[1])

    data = context.user_data["current_receipt"]
    selected_product = next((p for p in data["products"] if p["id"] == selected_product_id), None)
    
    # Update context with selected product
    if selected_product:
        context.user_data['current_receipt']['selected_product'] = selected_product

        # Text for product details
        text = f"Название продукта: {selected_product['name']}\n\n"
        text += f"Количество: {selected_product['quantity']}\n\n"
        text += f"Категория: {selected_product['category']}"
        
        await delete_message_by_id(update, context, 'product_message_id')

        await send_message(update, context, text="Выберите что сделать с продуктом", reply_markup=confirm_cancel_kb()) 
        # Send message with inline keyboard
        product_message = await query.message.reply_text(
            text=text,
            reply_markup=product_overview_kb(selected_product_id)
        )
        context.user_data['product_message_id'] = product_message.id
    else:
        await query.edit_message_text("Продукт не найден.")


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['current_receipt'].pop('selected_product', None)

    await delete_message_by_id(update, context, 'product_message_id')
    await delete_message_by_id(update, context, "receipt_message_id")

    await update.message.reply_text(
        "Назад к списку продуктов.",
    )
    await products_list_pag_callback(update, context)

menu_options: Dict[str, OptionHandler] = {
        "🔙 Назад": back
        }



async def handle_category_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the product ID from callback data
    product_id = int(update.callback_query.data.split('#')[1])
    logger.debug(f"{product_id} is product_id")
    
    # Store product_id in user_data for the category selection handler
    context.user_data["editing_product_id"] = product_id
    
    # Find product and remove from database if it was from db
    product = next(
        (p for p in context.user_data["current_receipt"]["products"] 
         if p["id"] == product_id),
        None
    )
    logger.debug(f"product is {product}")
    
    if product:
        product_names = [product["name"]]
        grpc_client = GRPCClient()
        response = await grpc_client.top_5_products(json.dumps(product_names, ensure_ascii=False))
        categories = json.loads(response.data)
        reply_markup = categories_kb(categories)
        context.user_data["available_categories"] = categories
        await update.callback_query.edit_message_text(
            text="Пожалуйста, выберите категорию",
            reply_markup=reply_markup
        )

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    
    # Get category index from callback data
    category_idx = int(update.callback_query.data.split('#')[1])
    # Get the actual category from stored list
    selected_category = context.user_data["available_categories"][category_idx]
    product_id = context.user_data.get("editing_product_id")

    if product_id is not None:
        # Find product in current receipt
        product = next(
            (p for p in context.user_data["current_receipt"]["products"] 
             if p["id"] == product_id),
            None
        )
        
        if product:
            # Update category in memory
            product["category"] = selected_category
            
            # If product is from database, update it there as well
            if product.get("from_db") is True:
                success = await update_product_category(product_id, selected_category)
                if not success:
                    logger.error(f"Failed to update category in database for product {product_id}")
            
                        # Clean up temporary data
            del context.user_data["editing_product_id"]
            del context.user_data["available_categories"]
            
            # Send confirmation message
            await update.callback_query.edit_message_text(
                text=f"Категория изменена на: {selected_category}"
            )
            
            # Update the product list display
            await products_list_pag_callback(update, context)
        else:
            await update.callback_query.edit_message_text(
                text="Продукт не найден"
            )
    else:
        await update.callback_query.edit_message_text(
            text="Произошла ошибка при изменении категории"
        )


async def handle_product_removal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle product removal from the current receipt."""
    await update.callback_query.answer()
    
    # Get the product ID from callback data
    product_id = int(update.callback_query.data.split('#')[1])
    
    # Find product and remove from database if it was from db
    product = next(
        (p for p in context.user_data["current_receipt"]["products"] 
         if p["id"] == product_id and p.get("from_db") is True),
        None
    )
    if product:
        await remove_product(product["id"])
    
    # Remove product from the current receipt list
    context.user_data['current_receipt']['products'] = [
        p for p in context.user_data['current_receipt']['products'] 
        if p["id"] != product_id
    ]
    await product_overview_callback(update, context)

    # Clear the selected product
    context.user_data["current_receipt"]["selected_product"] = None
    
    await update.callback_query.edit_message_text("Продукт удален из списка.")
    
    # Update the product list display
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
    application.add_handler(CallbackQueryHandler(handle_product_removal, pattern=r"^remove_product#\d+$"))
    application.add_handler(CallbackQueryHandler(handle_category_edit, pattern=r"^edit_category#\d+$"))
    application.add_handler(CallbackQueryHandler(
    handle_category_selection, 
    pattern="^set_category#"
    ))

    logger.debug("Добавлены product overview handlers")



