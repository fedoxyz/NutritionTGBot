from logger import logger

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from db import db, User
from sqlalchemy.future import select
from keyboards import main_kb
from utils.state_manager import set_current_state
from utils.message_utils import send_message
from utils.chat_filters import private_chat_only
from typing import Any

first_message = """
🎉 *Добро пожаловать, {username}! Я помогу тебе* 📊 *отследить и улучшить твое питание!*

Вот что я умею:
🍎 *Веду запись* твоих продуктов  
🧮 *Считаю химический состав*: калории, белки, жиры и углеводы  
📈 *Вывожу индекс* твоего питания  
📊 *Провожу анализ* и создаю отчеты о продуктовой корзине  
💡 *Даю рекомендации* для поддержания баланса необходимых нутриентов

🚀 *Как использовать бота:*

1️⃣ *Загрузи чек* из магазина в JSON-формате:  
   - 📱 *Скачай и открой* официальное приложение *«Проверка чеков ФНС»* – [Google Play](https://play.google.com/store/apps/details?id=ru.fns.billchecker), [App Store](https://apps.apple.com/ru/app/%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0-%D1%87%D0%B5%D0%BA%D0%BE%D0%B2-%D1%84%D0%BD%D1%81-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8/id1169353005) или [RuStore](https://www.rustore.ru/catalog/app/ru.fns.billchecker.mobile.android)  
   - 🔑 *Пройди авторизацию* (можно по номеру телефона)  
   - 📷 *Сканируй QR-код* чека (включи доступ к камере в настройках смартфона)  
   - 📤 *После сканирования* на экране отобразится информация о товарах. Нажми:  
     «Действия с чеком» → «Поделиться» → «JSON» → «Telegram» → выбери наше приложение.

2️⃣ *Альтернативные способы ввода информации:*  
   - ✍️ *Напиши текстом*, например: «хлеб ржаной 550 г, сметана 20% 200 г»  
   - 📸 *Сделай фотографию* чека и отправь ее боту  
   - 🎤 *Запиши голосовое сообщение* с названием продукта и его весом (в разработке)

3️⃣ *Для получения отчетов* используй команды из меню.

🤖 *Я активно учусь и совершенствуюсь для повышения качества работы!*  
*Если я где-то ошибся, сообщи мне* – так ты поможешь мне стать лучше и полезнее!

✨ *Теперь ты готов начать!* Загружай свои чеки и следи за своим питанием вместе со мной!
"""
start_message = "Добро пожаловать снова!" # Сообщение пользователям
 

@private_chat_only
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    user = update.effective_user
    if user: 
        user_id = user.id
        set_current_state(context, 0)
        async with db.session() as session:
            # Check if user already exists
            logger.debug(f"ID пользователя {user_id}")
            result = await session.execute(select(User).where(User.telegram_id == user.id))
            existing_user = result.scalar_one_or_none()
            
            if existing_user is None:
                logger.debug("Пользователь не существует")
                # User doesn't exist, create a new user
                new_user = User(telegram_id=user.id, username=user.username)
                session.add(new_user)
                text = first_message.format(username=user.username or "дорогой пользователь")
                await session.commit()
            else:
                text = start_message

        if update.message:
            await send_message(update, context, text, reply_markup=main_kb(), parse_mode='Markdown', disable_web_page_preview=True )
        elif update.callback_query and update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=main_kb()
            )
        
    return ConversationHandler.END 

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle any errors by resetting state and calling /start"""
    logger.error(f"Error occurred: {context.error}")
    
    try:
        if update and update.effective_chat:
            # Reset user data
            if context.user_data:
                context.user_data.clear()
            
            # Trigger /start command
            await update.effective_message.reply_text(
                "Произошла ошибка. Начинаем сначала..."
            )
            await start_handler(update, context)
    except Exception as e:
        logger.error(f"Error in error handler: {e}")

def setup_start_handler(application):
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(MessageHandler(
        filters.Regex("^(Главное меню)$"),
        start_handler
    ))
    application.add_error_handler(error_handler)
    logger.debug("Start handlers added");
