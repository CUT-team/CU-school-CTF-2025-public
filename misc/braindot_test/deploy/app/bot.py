import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from handlers import handlers
from db.db_session import global_init
import asyncio
import logging
from config import Config

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=Config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Запустить бота"),
            types.BotCommand(command="menu", description="Перейти в главное меню"),
            types.BotCommand(command="clear_data", description="Очистить данные"),
        ]
    )

    dp = Dispatcher()
    dp.include_routers(*handlers)
    await dp.start_polling(bot)

if __name__ == '__main__':
    global_init(f"postgresql+psycopg2://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}")
    asyncio.run(main())
    