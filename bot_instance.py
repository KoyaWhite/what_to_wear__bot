# bot_instance.py
from aiogram import Bot, Dispatcher

from API_KEYS import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()