import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set — скопируй .env.example в .env и заполни токен")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

AI_ENABLED: bool = os.getenv("AI_ENABLED", "false").lower() == "true"
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
