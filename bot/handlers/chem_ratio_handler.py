from logger import logger
import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from typing import Dict, Callable, Awaitable
from utils.message_utils import send_message
from utils.chat_filters import private_chat_only
from keyboards.chem_ratio_kb import nutrition_kb

OptionHandler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

async def chem_ratio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Пожалуйста, выберите раздел на клавиатуре"
    await send_message(update, context, text, reply_markup=nutrition_kb()) 

async def vitaminas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Здесь будет таблица с потребляемыми витаминами"
    await send_message(update, context, text, reply_markup=nutrition_kb())

async def minerals(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Здесь будет таблица с потребляемыми минералами"
    await send_message(update, context, text, reply_markup=nutrition_kb())

async def amino_acid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Здесь будет таблица с потребляемыми аминокислотами"
    await send_message(update, context, text, reply_markup=nutrition_kb())

async def fats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Здесь будет таблица с потребляемыми жирами"
    await send_message(update, context, text, reply_markup=nutrition_kb())

async def hydrocarbons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Здесь будет таблица с потребляемыми углеводами"
    await send_message(update, context, text, reply_markup=nutrition_kb())

async def psyched_substances(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Здесь будет таблица с потребляемыми психоактивными веществами"
    await send_message(update, context, text, reply_markup=nutrition_kb())

menu_options: Dict[str, OptionHandler] = {
    "Химсостав рациона": chem_ratio,
    "Витамины": vitaminas,
    "Минералы": minerals,
    "Аминокислоты": amino_acid,
    "Состав жиров": fats,
    "Состав углеводов": hydrocarbons,
    "Психоактивные вещества": psyched_substances,
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

def setup_chem_ratio_handlers(application):
    filter = filters.Regex('^(' + '|'.join(map(re.escape, menu_options.keys())) + ')$')
    application.add_handler(MessageHandler(filter & ~filters.COMMAND, handler))
    logger.debug("Добавлены chem ratio handlers")


