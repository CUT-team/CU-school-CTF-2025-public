from aiogram import types, Router

from config import Config

router = Router()

@router.message()
async def admin_message(message: types.Message):
    if message.from_user.id == Config.ADMIN_ID:
        reply_to = message.reply_to_message
        if reply_to:
            data = reply_to.text.split(":")
            user_id = int(data[0])
            await message.bot.send_message(
                user_id,
                "Тебе пришел ответ:\n\n" + message.text
            )
        else:
            pass
    else:
        await message.answer("Я тебя не понимаю")