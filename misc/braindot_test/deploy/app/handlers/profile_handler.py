import re
from venv import logger
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.back2menu_keyboard import get_back2menu_keyboard
from keyboards.usedefault_keyboard import use_default_keyboard
from keyboards.profile_keyboard import get_profile_keyboard
from db.service import get_user, update_user
from utils.ssti_checker import is_safe_input
router = Router()

class ProfileEditStates(StatesGroup):
    EDIT_STATE = State()

@router.callback_query(F.data == "profile")
async def cmd_profile(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)

    if not user:
        await callback.message.answer("Ты не зарегестрирован. Заходи в /start")
        return

    await callback.message.answer(
        text=f"<b>Профиль</b>\n<b>Имя:</b> {user.first_name}\n<b>Фамилия:</b> {user.last_name}\n<b>Инфо:</b> {user.bio}",
        reply_markup=get_profile_keyboard())
    await callback.message.delete()

@router.callback_query(F.data.startswith("profile:"))
async def profile_actions(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split(":")[1]
    await state.set_state(ProfileEditStates.EDIT_STATE)
    await state.update_data(action=action)

    await callback.message.answer("Введите новое значение.", reply_markup=use_default_keyboard)
    await callback.message.delete()

@router.message(ProfileEditStates.EDIT_STATE)
async def process_edit(message: types.Message, state: FSMContext):

    user_input = message.text
    if not user_input:
        await message.answer("Пустое значение. Попробуй ещё раз.")
        return
    
    data = await state.get_data()
    action = data.get('action')
    user = get_user(message.from_user.id)

    if user_input == "Пробить по базе.":
        if action == "first_name":
            user.first_name = message.from_user.first_name
        elif action == "last_name":
            user.last_name = message.from_user.last_name
        elif action == "bio":
            chat = await message.bot.get_chat(message.from_user.id)
            user.bio = chat.bio
            

        update_user(user=user)
        await message.answer("Изменения сохранены.", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Пора домой.", reply_markup=get_back2menu_keyboard())
        await state.clear()
        return
    
    match action:
        case "first_name":
            check = re.match(r"^[a-zA-Zа-яА-Я]+$", user_input)
            if not check or len(user_input) not in range(2, 40):
                await message.answer("Имя должно состоять только из букв.")
                return
        case "last_name":
            check = re.match(r"^[a-zA-Zа-яА-Я]+$", user_input)
            if not check or len(user_input) not in range(2, 40):
                await message.answer("Фамилия должна состоять только из букв.")
                return
        case "bio":
            if not is_safe_input(user_input) or len(user_input) > 400:
                await message.answer("Полегче с выражениями брат. У нас тут такое не используют.")
                return
    setattr(user, action, user_input)
    update_user(user=user)
    await message.answer("Изменения сохранены.", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Пора домой.", reply_markup=get_back2menu_keyboard())
    await state.clear()
            