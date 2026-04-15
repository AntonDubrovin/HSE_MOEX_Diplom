import asyncio
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from src.tg_bot.handlers import router

load_dotenv()


async def main():
    bot = Bot(token=os.getenv("TG_BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
