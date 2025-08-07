# keyboards/city_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

CITIES = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
    "Нижний Новгород", "Челябинск", "Самара", "Омск", "Ростов-на-Дону",
    "Уфа", "Красноярск", "Воронеж", "Пермь", "Волгоград"
]

def get_city_keyboard():
    keyboard = []
    row = []
    for city in CITIES:
        row.append(KeyboardButton(text=city))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)