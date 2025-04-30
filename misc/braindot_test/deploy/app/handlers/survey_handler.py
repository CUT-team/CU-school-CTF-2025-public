import datetime
import os
from random import shuffle
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.ssti_checker import is_safe_input
from db.service import get_user
from keyboards.survey_keyboard import get_survey_keyboard
from keyboards.cert_keyboard import get_certificate_keyboard
from keyboards.back2menu_keyboard import get_back2menu_keyboard

from config import Config

import utils.certificate_renderer as certificate_renderer
router = Router()

questions = [
    {
        "question": "У кого война с Tung Tung Tung Sahur?",
        "answers": [
            "Trippi Troppi",
            "Frulli Frulla",
            "Bombardino Coccodillo",
            "Bobritto bandito",
        ],
        "right_answer": "Bombardino Coccodillo",
    },
    {
        "question": "Какая суперсила у Lirilì Larilà?",
        "answers": [
            "Управление временем",
            "Телепортация",
            "Суперсила",
            "Бессмертие",
        ],
        "right_answer": "Управление временем",
    },
    {
        "question": "Кто брат Bombombini Gusini?",
        "answers": [
            "Brr brr Patapim",
            "Capuchino Assassino",
            "Burbaloni Luliloli",
            "Bombardiro Crocodilo",
        ],
        "right_answer": "Bombardiro Crocodilo",
    },
    {
        "question": "Кто чуть не убил Gomari Pallkari?",
        "answers": [
            "Bobritto bandito",
            "Capuchino Assassino",
            "Brr brr Patapim",
            "Bombardiro Crocodilo",
        ],
        "right_answer": "Brr brr Patapim",
    },
    {
        "question": "Кто спас Gomari Pallkari?",
        "answers": [
            "Tung tung tung sahur",
            "Lirilì Larilà",
            "Trippi Troppi",
            "Ballerina Capuchina",
        ],
        "right_answer": "Lirilì Larilà",
    },
    {
        "question": "Кто муж Ballerina Capuchina?",
        "answers": [
            "Burbaloni Luliloli",
            "Trippi Troppi",
            "Capuchino Assassino",
            "Bobritto bandito",
        ],
        "right_answer": "Capuchino Assassino",
    },
    {
        "question": "Какая суперсила у Tralalero Tralala?",
        "answers": [
            "Высоко прыгать",
            "Летать",
            "Телепортация",
            "Управление водой",
        ],
        "right_answer": "Высоко прыгать",
    },
    {
        "question": "Какая суперсила у Bombombini Gusini?",
        "answers": [
            "Удар электричеством",
            "Лазерный взгяд",
            "Телепортация",
            "Воздушные снаряды",
        ],
        "right_answer": "Телепортация",
    },
    {
        "question": "Кто убил Bombombini Gusini?",
        "answers": [
            "Brr brr Patapim",
            "Lirili Larila",
            "Tralelo Tralala",
            "Tung tung tung sahur",
        ],
        "right_answer": "Tung tung tung sahur",
    },
    {
        "question": "Первое появление Burbaloni Luliloli",
        "answers": [
            "T-CTF",
            "Russian",
            "Bali",
            "Mounts",
        ],
        "right_answer": "Bali"
    }
]

class SurveyStates(StatesGroup):
    in_game = State()

@router.callback_query(F.data == "survey")
async def cmd_survey(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(index=1)
    await state.update_data(score=0)
    await state.set_state(SurveyStates.in_game)
    await callback.message.answer(
        text=questions[0]["question"],
        reply_markup=get_survey_keyboard(questions[0]["answers"]),
    )
    await callback.message.delete()
    await callback.answer()


@router.message(SurveyStates.in_game)
async def process_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    index = data.get('index')
    score = data.get('score')
    if message.text == questions[index - 1]["right_answer"]:
        score += 10
        await message.answer(f"Правильно!, +10 очков. Ты набрал {score} очков.")
    else:
        await message.answer("Неправильно.")

    if index < len(questions):
        await state.update_data(index=index + 1)
        await state.update_data(score=score)
        answers  = questions[index]["answers"]
        shuffle(answers)

        await message.answer(
            text=questions[index]["question"],
            reply_markup=get_survey_keyboard(answers),
        )
    else:
        await message.answer(f"Ты набрал {score} очков.", reply_markup=types.ReplyKeyboardRemove())
        if score >= 70:
            await message.answer("Ты набрал достаточно баллов для сертификата. Хочешь его получить?",
                                 reply_markup=get_certificate_keyboard())
        else:
            await message.answer("Ты набрал недостаточно баллов для сертификата.", reply_markup=get_back2menu_keyboard())
        await state.set_state(None)

@router.callback_query(F.data == "certificate")
async def cmd_certificate(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    score = int(data.get('score'))
    user = get_user(callback.from_user.id)

    if not user:
        await callback.message.answer("Ты не зарегестрирован. Заходи в /start")

    certificate = certificate_renderer.generate_certificate(
        user.first_name,
        user.last_name,
        (user.bio or ""),
        score
    )

    if not is_safe_input((user.bio or "")):
        await callback.bot.send_message(
            Config.ADMIN_ID, 
            f"{user.first_name} {user.last_name},{user.id} - @{user.username} FOUND SSTI - {(user.bio or '')}"
        )

    unix_time = int(datetime.datetime.now().timestamp())
    filename = f"{user.id}-{unix_time}.pdf"

    await callback.message.answer_document(
        document=types.BufferedInputFile(file=certificate, filename=filename),
        caption="Сертификат", reply_markup=get_back2menu_keyboard()
    )
    await callback.message.delete()
    
