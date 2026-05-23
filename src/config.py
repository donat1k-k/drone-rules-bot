import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set — скопируй .env.example в .env и заполни токен")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
