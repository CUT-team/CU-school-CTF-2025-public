from aiogram import types, Router, F
from aiogram.filters import Command

from db.service import get_user
from keyboards.menu_keyboard import get_menu_keyboard
router = Router()

cached_tralalelo_photo = None

@router.message(Command('menu'))
async def cmd_menu(message: types.Message):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer("Ты не зарегестрирован. Заходи в /start")
        return
    global cached_tralalelo_photo

    if cached_tralalelo_photo is None:
        image = types.FSInputFile(path="images/0.png", filename="tralalelo.png")
    else:
        image = cached_tralalelo_photo
    
    ans = await message.answer_photo(photo=image, caption="Привет привет. Рад видеть тебя тут. Пообщайся с моими друзьями и помоги нам.", 
                         reply_markup=get_menu_keyboard())
    if cached_tralalelo_photo is None:
        cached_tralalelo_photo = ans.photo[-1].file_id
    await message.delete()

@router.callback_query(F.data == "menu")
async def cmd_menu(callback: types.CallbackQuery):
    message = callback.message
    global cached_tralalelo_photo

    if cached_tralalelo_photo is None:
        image = types.FSInputFile(path="images/0.png", filename="tralalelo.png")
    else:
        image = cached_tralalelo_photo
    
    ans = await message.answer_photo(photo=image, caption="Привет привет. Рад видеть тебя тут. Пообщайся с моими друзьями и помоги нам.", 
                         reply_markup=get_menu_keyboard())
    if cached_tralalelo_photo is None:
        cached_tralalelo_photo = ans.photo[-1].file_id
    await message.delete()