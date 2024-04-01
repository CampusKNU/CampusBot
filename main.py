import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher

from src.handlers.user import router as user_router
from src.bot import bot

dp = Dispatcher()


async def main() -> None:
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
