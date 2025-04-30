from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_view_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="<-", callback_data="view:prev"),
        InlineKeyboardButton(text="->", callback_data="view:next")
    )
    builder.row(
        InlineKeyboardButton(text="Написать сообщение", callback_data="view:send_message")
    )
    builder.row(
        InlineKeyboardButton(text="Меню", callback_data="menu")
    )
    return builder.as_markup()