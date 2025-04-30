from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_profile_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Имя", callback_data="profile:first_name"),
        InlineKeyboardButton(text="Фамилию", callback_data="profile:last_name"),
        InlineKeyboardButton(text="Инфо", callback_data="profile:bio")
    )
    builder.row(
        InlineKeyboardButton(text="Меню", callback_data="menu")
    )
    return builder.as_markup()