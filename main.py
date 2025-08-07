# main.py
import asyncio
from bot_instance import dp, bot

# Импортируем роутеры
from handlers.weather_handlers import router as weather_router
from handlers.donate_handler import router as donate_router  # новый

from flask import Flask
import threading

# === Flask для keep-alive ===
app = Flask('')

@app.route('/')
def home():
    return 'Bot is alive!'

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# === Главная функция запуска ===
async def main():
    # Подключаем все роутеры
    dp.include_router(weather_router)
    dp.include_router(donate_router)  # добавили обработчик донатов

    print("Бот запущен... Ожидаем команды")
    await dp.start_polling(bot)

# === Запуск ===
if __name__ == "__main__":
    keep_alive()  # Запускаем веб-сервер в фоне
    asyncio.run(main())