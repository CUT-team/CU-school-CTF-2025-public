from collections import defaultdict
import logging
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.back2menu_keyboard import get_back2menu_keyboard
from config import Config

from keyboards.view_keyboard import get_view_keyboard
from db.mock import Mock
from db.service import get_mock
router = Router()

cached_photos = defaultdict(str)

class ViewStates(StatesGroup):
    send_message = State()

@router.callback_query(F.data == "view")
async def cmd_view(callback: types.CallbackQuery, state: FSMContext):
    global cached_photos
    await state.clear()
    await state.update_data(current_index=0)

    mock: Mock = get_mock(0)
    if not cached_photos[mock.id]:
        photo = await callback.bot.send_photo(Config.ADMIN_ID, 
                                              photo=types.FSInputFile(
                                                  path=f"images/{mock.id}.png",
                                                  filename=f"{mock.id}.png"
                                              ))
        cached_photos[mock.id] = photo.photo[-1].file_id
        await photo.delete()
        photo = cached_photos[mock.id]
    else:
        photo = cached_photos[mock.id]
    
    await callback.message.answer_photo(photo=photo,
                                        caption=f"{mock.first_name} {mock.last_name}\nНабрал {mock.score} очков\n{mock.info}",
                                        reply_markup=get_view_keyboard())
    await callback.message.delete()
    
@router.callback_query(F.data.startswith("view:"))
async def view_actions(callback: types.CallbackQuery, state: FSMContext):
    global cached_photos
    action = callback.data.split(":")[1]
    data = await state.get_data()
    index = data.get("current_index", 0)
    if action == "next":
        index = min(index + 1, 8)
    elif action == "prev":
        index = max(index - 1, 0)
    elif action == "send_message":
        await callback.message.answer("Введите сообщение.")
        await state.set_state(ViewStates.send_message)
        await callback.message.delete()
        return

    await state.update_data(current_index=index)

    mock: Mock = get_mock(index)
    logging.warning(f"Mock id: {mock.id} {index}")
    if not cached_photos[mock.id]:
        photo = await callback.bot.send_photo(Config.ADMIN_ID, 
                                              photo=types.FSInputFile(
                                                  path=f"images/{mock.id}.png",
                                                  filename=f"{mock.id}.png"
                                              ))
        cached_photos[mock.id] = photo.photo[-1].file_id
        await photo.delete()
        photo = cached_photos[mock.id]
    else:
        photo = cached_photos[mock.id]
    
    await callback.message.edit_media(media=types.InputMediaPhoto(media=photo))
    await callback.message.edit_caption(
        caption=f"[{index+1}/9]\n{mock.first_name} {mock.last_name}\nНабрал {mock.score} очков\n{mock.info}",
        reply_markup=get_view_keyboard()
    )

@router.message(ViewStates.send_message)
async def send_message(message: types.Message, state: FSMContext):
    text = message.text
    await message.bot.send_message(
        Config.ADMIN_ID,
        f"{message.from_user.id}:{message.from_user.username}:{text}"
    )
    await message.answer("Сообщение отправлено. Будем ждать ответа.", reply_markup=get_back2menu_keyboard())
    await state.clear()
    