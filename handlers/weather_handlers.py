# handlers/weather_handlers.py
from aiogram import types, Router
from aiogram.filters import Command

from keyboards.city_keyboard import get_city_keyboard
from services.weather_service import get_weather
from services.outfit_service import get_outfit_recommendation

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Выбери город из списка, чтобы узнать погоду и что надеть:",
        reply_markup=get_city_keyboard()
    )

@router.message()
async def handle_city_selection(message: types.Message):
    city = message.text.strip()

    from keyboards.city_keyboard import CITIES
    if city not in CITIES:
        await message.answer(
            "Пожалуйста, выбери город из списка ниже:",
            reply_markup=get_city_keyboard()
        )
        return

    await message.answer(f"🔍 Получаем погоду в городе {city}...")

    temp, city_name = get_weather(city)
    if temp is None:
        await message.answer(f"❌ {city_name}")
        return

    header, outfit = get_outfit_recommendation(temp)

    result = (
        f"📍 Город: {city_name}\n"
        f"🌡️ Температура: {temp}°C\n"
        f"{header}\n\n"
        f"👗 Что надеть:\n{outfit}"
    )
    await message.answer(result)