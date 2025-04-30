from aiogram import types

use_default_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Пробить по базе.")
        ]
    ], resize_keyboard=True
)