import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.config import BOT_TOKEN, LOG_LEVEL
from src.bot.handlers import common, topics


async def main() -> None:
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(common.router)
    dp.include_router(topics.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
