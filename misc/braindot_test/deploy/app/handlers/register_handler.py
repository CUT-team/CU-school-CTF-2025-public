import re
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.user import User
from db.service import get_user, create_user
from keyboards.usedefault_keyboard import use_default_keyboard
from utils.ssti_checker import is_safe_input

router = Router()

class RegisterStates(StatesGroup):
    FIRST_NAME = State()
    LAST_NAME = State()
    BIO = State()
    PHOTO = State()



@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user = get_user(message.from_user.id)
    if user:
        await message.answer("Ты уже зарегестрирован. Заходи в /menu")
    else:
        await state.set_state(RegisterStates.FIRST_NAME)
        await message.answer("Хэй хэй дружище. Полегче. Сначала назовись.", 
                             reply_markup=use_default_keyboard)

@router.message(RegisterStates.FIRST_NAME)
async def process_first_name(message: types.Message, state: FSMContext):
    name = message.text
    if name == "Пробить по базе.":
        name = message.from_user.first_name
    if not re.match(r"^[a-zA-Zа-яА-Я]+$", name) or len(name) not in range(2, 40):
        await message.answer("Имя должно состоять только из букв.")
        return
    await state.update_data(first_name=name)
    await state.set_state(RegisterStates.LAST_NAME)
    await message.answer("А по батюшке как?.")

@router.message(RegisterStates.LAST_NAME)
async def process_last_name(message: types.Message, state: FSMContext):
    name = message.text
    if name == "Пробить по базе.":
        name = message.from_user.last_name
    if not name:
        name = "Безфамильный"
    if not re.match(r"^[a-zA-Zа-яА-Я]+$", name) or len(name) not in range(2, 40):
        await message.answer("Фамилия должна состоять только из букв.")
        return
    await state.update_data(last_name=name)
    await state.set_state(RegisterStates.BIO)
    await message.answer("Кто ты по жизни? Чем занимаешься?")

@router.message(RegisterStates.BIO)
async def process_bio(message: types.Message, state: FSMContext):
    bio = message.text
    if bio == "Пробить по базе.":
        chat = await message.bot.get_chat(message.from_user.id)
        bio = chat.bio
    elif not is_safe_input(bio):
        await message.answer("Полегче с выражениями брат. У нас тут такое не используют.")
        return
    await state.update_data(bio=bio)
    data = await state.get_data()
    create_user(User(
        id=message.from_user.id, username=message.from_user.username, **data
    ))
    await message.answer("Ты зарегестрирован. Заходи в /menu", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

    