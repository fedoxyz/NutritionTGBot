import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

IS_DEBUG = os.getenv("DEBUG")

GRPC_SERVER = os.getenv("GRPC_SERVER")

