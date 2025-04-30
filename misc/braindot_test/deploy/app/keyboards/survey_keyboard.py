from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_survey_keyboard(vars:list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(
        *[KeyboardButton(text=var) for var in vars]
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)