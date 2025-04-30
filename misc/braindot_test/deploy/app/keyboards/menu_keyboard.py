from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Профиль 👤", callback_data="profile"),
        InlineKeyboardButton(text="Опрос 📃", callback_data="survey")
    )
    builder.row(
        InlineKeyboardButton(text="Просмотр анкет 📩", callback_data="view")
    )
    return builder.as_markup()