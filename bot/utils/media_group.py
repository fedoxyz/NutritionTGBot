import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from logger import logger

MEDIA_GROUP_TIMEOUT = 1.0  # 1 second timeout

async def handle_media_group(context: ContextTypes.DEFAULT_TYPE, message, rec_id, send_function):
    media_group_id = message.media_group_id
    if 'media_groups' not in context.chat_data:
        context.chat_data['media_groups'] = {}
    
    if media_group_id not in context.chat_data['media_groups']:
        context.chat_data['media_groups'][media_group_id] = {
            'messages': [],
            'timer': datetime.now() + timedelta(seconds=MEDIA_GROUP_TIMEOUT)
        }
    
    context.chat_data['media_groups'][media_group_id]['messages'].append(message)
    
    if len(context.chat_data['media_groups'][media_group_id]['messages']) == 1:
        asyncio.create_task(process_media_group_after_timeout(context, media_group_id, rec_id, send_function))

async def process_media_group_after_timeout(context, media_group_id, rec_id, send_function):
    await asyncio.sleep(MEDIA_GROUP_TIMEOUT)
    
    if media_group_id in context.chat_data['media_groups']:
        media_group = context.chat_data['media_groups'][media_group_id]
        messages = media_group['messages']
        photos = [m.photo[-1].file_id for m in messages if m.photo]
        caption = messages[0].caption or "Фотографии"
        logger.debug(caption)
        await send_function(context.bot, rec_id, photos, caption)
        
        del context.chat_data['media_groups'][media_group_id]
    else:
        logger.warning(f"Media group {media_group_id} не была найдена после timeout")
