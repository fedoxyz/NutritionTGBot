#/usr/bin/env python3
from logs.logger import logger
from db import init_db
import asyncio
from telegram.ext import ApplicationBuilder
from handlers import setup_all_handlers
from config import TOKEN

async def main():
    await init_db()

    app = ApplicationBuilder().token(TOKEN).build()
    setup_all_handlers(app)

    logger.info("Бот запускается...")

    await app.initialize()
    await app.start()

    try:
        await app.updater.start_polling()
        logger.info("Бот запущен")
        # Keep the bot running until interrupted
        await asyncio.Event().wait()
    finally:
        logger.info("Остановка бота...")
        await app.stop()
        await app.shutdown()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Возникла непредвиденная ошибка: {e}")
