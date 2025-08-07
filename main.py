# main.py
import asyncio
from bot_instance import dp, bot
from handlers.weather_handlers import router
from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return 'Bot is alive!'

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

async def main():
    # Подключаем роутер
    dp.include_router(router)
    
    print("Бот запущен... Ожидаем /start")
    await dp.start_polling(bot)

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())