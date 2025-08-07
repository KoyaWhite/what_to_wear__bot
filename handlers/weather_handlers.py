# handlers/weather_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.city_keyboard import get_city_keyboard, SUPPORT_BUTTON_TEXT, OTHER_CITY_BUTTON_TEXT, CITIES
from services.weather_service import get_weather
from services.outfit_service import get_outfit_recommendation
from keyboards.donate_keyboard import donate_kb

router = Router()

# Состояние: ожидаем ввод города
waiting_for_city = set()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Выбери город из списка или введи любой город вручную.",
        reply_markup=get_city_keyboard()
    )


@router.message(F.text == SUPPORT_BUTTON_TEXT)
async def handle_support(message: Message):
    await message.answer(
        "Спасибо, что хочешь поддержать бота! 💖\n\n"
        "Твоя поддержка помогает оставлять бота бесплатным и развивать его.\n\n"
        "Выберите удобный способ:",
        reply_markup=donate_kb
    )


@router.message(F.text == OTHER_CITY_BUTTON_TEXT)
async def ask_for_city(message: Message):
    waiting_for_city.add(message.from_user.id)
    await message.answer(
        "Введите название города (на русском или английском):",
        reply_markup=None  # временно убираем клавиатуру
    )


@router.message()
async def handle_city_selection(message: Message):
    user_id = message.from_user.id
    city = message.text.strip()

    # Если это команда — игнорируем
    if city.startswith("/"):
        return

    # Если пользователь ожидает ввод города
    if user_id in waiting_for_city:
        waiting_for_city.discard(user_id)
        reply_markup = get_city_keyboard()  # возвращаем клавиатуру
    else:
        # Если это кнопка из списка — используем как есть
        if city in CITIES:
            reply_markup = get_city_keyboard()
        else:
            # Это свободный ввод — не возвращаем клавиатуру сразу
            reply_markup = get_city_keyboard()  # можно оставить

    # Обработка поддержки (на всякий случай)
    if city == SUPPORT_BUTTON_TEXT:
        await handle_support(message)
        return

    # Запрашиваем погоду
    temp, city_name = get_weather(city)
    if temp is None:
        await message.answer(
            f"❌ {city_name}\n\n"
            "Попробуйте выбрать из списка или ввести корректное название.",
            reply_markup=reply_markup
        )
        return

    header, outfit = get_outfit_recommendation(temp)
    result = (
        f"📍 Город: {city_name}\n"
        f"🌡️ Температура: {temp}°C\n"
        f"{header}\n\n"
        f"🔸 Что надеть:\n{outfit}"
    )
    await message.answer(result, reply_markup=reply_markup)