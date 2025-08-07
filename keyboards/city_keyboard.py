# keyboards/city_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Список популярных городов России
CITIES = [
    "Москва",
    "Санкт-Петербург",
    "Новосибирск",
    "Екатеринбург",
    "Казань",
    "Нижний Новгород",
    "Челябинск",
    "Самара",
    "Омск",
    "Ростов-на-Дону",
    "Уфа",
    "Красноярск",
    "Воронеж",
    "Пермь",
    "Волгоград",
    "Краснодар"
]

# Кнопка поддержки
SUPPORT_BUTTON_TEXT = "⭐ Поддержать автора ⭐️"
OTHER_CITY_BUTTON_TEXT = "🌍 Другой город"

def get_city_keyboard():
    keyboard = []
    row = []

    # Добавляем города по 2 в ряд
    for city in CITIES:
        row.append(KeyboardButton(text=city))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    # Добавляем остаток (если нечётное количество)
    if row:
        keyboard.append(row)

    # Добавляем "Другой город"
    keyboard.append([
        KeyboardButton(text=OTHER_CITY_BUTTON_TEXT)
    ])

    # Добавляем кнопку "Поддержать автора" отдельной строкой
    keyboard.append([
        KeyboardButton(text=SUPPORT_BUTTON_TEXT)
    ])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False  # можно оставить клавиатуру
    )