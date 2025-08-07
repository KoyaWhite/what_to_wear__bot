# bot_instance.py
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

# Загружаем переменные из .env (только для локальной среды)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not BOT_TOKEN:
    raise ValueError("Не установлен BOT_TOKEN в переменных окружения")
if not OPENWEATHER_API_KEY:
    raise ValueError("Не установлен OPENWEATHER_API_KEY в переменных окружения")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()