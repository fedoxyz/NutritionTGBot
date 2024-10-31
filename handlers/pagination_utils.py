from logs.logger import logger
from telegram import Update
from telegram.ext import ContextTypes
from utils.message_utils import send_message, edit_message



async def handle_pagination(update: Update, context: ContextTypes.DEFAULT_TYPE, paginator_func, list_text: str, **kwargs) -> None:
    query = update.callback_query
    if query:
        await query.answer()
        logger.debug(f"query.data: {query.data}")
    user_id = update.effective_user.id
    page = int(query.data.split('#')[1]) if query and query.data else 1
    paginator = await paginator_func(update, context, user_id, page, **kwargs)
    text = f"{list_text}\nСтраница {page}"
    
    if query:
        return await edit_message(query, text=text, reply_markup=paginator.markup)
    else:
        return await send_message(update, context, text=text, reply_markup=paginator.markup)

async def handle_list_display(update: Update, context: ContextTypes.DEFAULT_TYPE, paginator_func, list_text: str) -> None:
    text = list_text
    user_id = update.effective_user.id
    paginator = await paginator_func(update, context, user_id, 1)
    if paginator:
        text += "\nСтраница 1"
        return await send_message(update, context, text, reply_markup=paginator.markup)
    else:
        text += "\nПусто"
        return await send_message(update, context, text)
