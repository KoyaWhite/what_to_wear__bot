# main.py
import asyncio
from bot_instance import dp, bot
from handlers.weather_handlers import router

async def main():
    # Подключаем роутер
    dp.include_router(router)
    
    print("Бот запущен... Ожидаем /start")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())