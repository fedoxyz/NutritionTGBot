from handlers.receipt_overview_handler import products_list_pag_callback
from logger import logger
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message
from utils.chat_filters import private_chat_only
from keyboards.data_source_kb import receipts_paginator, data_source_kb, products_paginator
from keyboards.paginator_kb import handle_pagination, handle_list_display


OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def receipts_list_pag_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_pagination(update, context, receipts_paginator, "Список чеков:")

#async def products_list_pag_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#    context.user_data['current_receipt'] = {
#            'products': data["products"],
#            'receipt_date': data["receipt_date"],
#            'current_page': 1,
#            'editing_mode': False,
#            'selected_product': None
#        }
#    await handle_pagination(update, context, products_paginator, "Список купленных продуктов:")

async def data_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Выберите опцию: "
    await send_message(update, context, text, reply_markup=data_source_kb()) 

async def how_to_receipts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = """1️⃣ *Загрузи чек* из магазина в JSON-формате:  
       - 📱 *Скачай и открой* официальное приложение *«Проверка чеков ФНС»* – [Google Play](https://play.google.com/store/apps/details?id=ru.fns.billchecker), [App Store](https://apps.apple.com/ru/app/%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0-%D1%87%D0%B5%D0%BA%D0%BE%D0%B2-%D1%84%D0%BD%D1%81-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8/id1169353005) или [RuStore](https://www.rustore.ru/catalog/app/ru.fns.billchecker.mobile.android)  
       - 🔑 *Пройди авторизацию* (можно по номеру телефона)  
       - 📷 *Сканируй QR-код* чека (включи доступ к камере в настройках смартфона)  
       - 📤 *После сканирования* на экране отобразится информация о товарах. Нажми:  
         «Действия с чеком» → «Поделиться» → «JSON» → «Telegram» → выбери наше приложение.

    2️⃣ *Альтернативные способы ввода информации:*  
       - ✍️ *Напиши текстом*, например: «хлеб ржаной 550 г, сметана 20% 200 г»  
       - 📸 *Сделай фотографию* чека и отправь ее боту  
       - 🎤 *Запиши голосовое сообщение* с названием продукта и его весом (в разработке)

    3️⃣ *Для получения отчетов* используй команды из главного меню (команда /start).
    """
    await send_message(update, context, text=text, reply_markup=data_source_kb(), parse_mode="Markdown", disable_web_page_preview=True)

async def receipts_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_list_display(update, context, receipts_paginator, "Список чеков:")

async def unrecognized_p_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Здесь будет список нераспознанных продуктов"
    await send_message(update, context, text, reply_markup=data_source_kb())

menu_options: Dict[str, OptionHandler] = {
    "Источники данных": data_source,
    "Как добавлять чеки": how_to_receipts,
    "Список чеков": receipts_list,
    "Список купленных продуктов": products_list_pag_callback,
    "Список нераспознанных продуктов": unrecognized_p_list,
}

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

def setup_data_source_handlers(application):
    filter = filters.Regex('^(' + '|'.join(map(re.escape, menu_options.keys())) + ')$')
    application.add_handler(MessageHandler(filter & ~filters.COMMAND, handler))
    application.add_handler(CallbackQueryHandler(receipts_list_pag_callback, pattern=r"^receipts_page#\d+$"))
    #application.add_handler(CallbackQueryHandler(products_list_pag_callback, pattern=r"^products_page#\d+$"))

    logger.debug("Добавлены menu handlers")


