from aiogram import types, Router
from aiogram.filters import Command
from config import Config
from db.service import delete_user
router = Router()

@router.message(Command('clear_data'))
async def clear_data_message(message: types.Message):
    delete_user(message.from_user.id)
    await message.answer("Данные очищены")