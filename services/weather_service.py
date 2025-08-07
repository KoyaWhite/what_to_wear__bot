# services/weather_service.py
import requests
import time
from bot_instance import OPENWEATHER_API_KEY

# Маппинг: кириллические названия → латиница
CITY_ALIASES = {
    "Москва": "Moscow",
    "Санкт-Петербург": "Saint Petersburg",
    "Новосибирск": "Novosibirsk",
    "Екатеринбург": "Yekaterinburg",
    "Казань": "Kazan",
    "Нижний Новгород": "Nizhny Novgorod",
    "Челябинск": "Chelyabinsk",
    "Самара": "Samara",
    "Омск": "Omsk",
    "Ростов-на-Дону": "Rostov-on-Don",
    "Уфа": "Ufa",
    "Красноярск": "Krasnoyarsk",
    "Воронеж": "Voronezh",
    "Пермь": "Perm",
    "Волгоград": "Volgograd",
    "Краснодар": "Krasnodar"
}

# Кэш: {город: (температура, city_name, timestamp)}
WEATHER_CACHE = {}
CACHE_TTL = 1200  # 30 минут (в секундах)

def get_weather(city: str):
    """
    Получает погоду из кэша (если актуальна) или из API.
    :param city: Название города
    :return: (температура, название города) или (None, сообщение_об_ошибке)
    """
    city = city.strip()
    if not city:
        return None, "Название города не может быть пустым."

    current_time = time.time()

    # Проверяем кэш
    if city in WEATHER_CACHE:
        temp, city_name, timestamp = WEATHER_CACHE[city]
        if current_time - timestamp < CACHE_TTL:
            print(f"[CACHE] Используем кэш для {city}: {temp}°C")
            return temp, city_name
        else:
            print(f"[CACHE] Кэш устарел для {city}, обновляем...")
            del WEATHER_CACHE[city]

    # Преобразуем в латиницу, если есть алиас
    city_for_api = CITY_ALIASES.get(city, city)

    # Шаг 1: Геокодирование
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {
        "q": city_for_api,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY
    }

    try:
        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        print(f"[DEBUG] Геозапрос: {geo_url}?q={city_for_api} → статус: {geo_response.status_code}")

        if geo_response.status_code == 200:
            data = geo_response.json()
            if not data:
                print(f"[ERROR] Город '{city_for_api}' не найден в OpenWeatherMap.")
                return None, "❌ Город не найден. Проверьте название и попробуйте снова."

            location = data[0]
            country = location.get("country")

            # Пропускаем любые города
            print(f"[INFO] Город найден: {location['name']} ({country})")

            lat = location["lat"]
            lon = location["lon"]
            city_name = location.get("local_names", {}).get("ru", location["name"])

            # Шаг 2: Получение погоды
            weather_url = "https://api.openweathermap.org/data/2.5/weather"
            weather_params = {
                "lat": lat,
                "lon": lon,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": "ru"
            }

            weather_response = requests.get(weather_url, params=weather_params, timeout=10)
            print(f"[DEBUG] Запрос погоды: {weather_url}?lat={lat}&lon={lon} → статус: {weather_response.status_code}")

            if weather_response.status_code == 200:
                temp = round(weather_response.json()["main"]["temp"])
                # Сохраняем в кэш
                WEATHER_CACHE[city] = (temp, city_name, current_time)
                print(f"[CACHE] Сохранено в кэш: {city} → {temp}°C")
                return temp, city_name

            elif weather_response.status_code == 401:
                print("[CRITICAL] Ошибка 401: Неверный или неактивированный API-ключ.")
                return None, "🔐 Ошибка авторизации. Проверьте ключ API."

            elif weather_response.status_code == 404:
                print(f"[ERROR] Погода для координат {lat},{lon} не найдена.")
                return None, "☁️ Данные о погоде недоступны."

            elif weather_response.status_code == 429:
                print("[ERROR] Превышен лимит запросов к OpenWeatherMap (429).")
                return None, "⏳ Слишком много запросов. Подождите минуту."

            else:
                print(f"[ERROR] Неожиданный код погоды: {weather_response.status_code}, тело: {weather_response.text}")
                return None, "⚠️ Ошибка при получении погоды."

        elif geo_response.status_code == 401:
            print("[CRITICAL] Ошибка 401 при геокодировании — проверьте OPENWEATHER_API_KEY.")
            return None, "🔐 Ошибка авторизации. Убедитесь, что API-ключ верный и активирован."

        elif geo_response.status_code == 429:
            print("[ERROR] Превышен лимит запросов к геокодеру (429).")
            return None, "⏳ Слишком много запросов. Подождите перед повторным запросом."

        else:
            print(f"[ERROR] Ошибка геокодера: {geo_response.status_code}, ответ: {geo_response.text}")
            return None, "🌐 Сервис временно недоступен."

    except requests.exceptions.Timeout:
        print("[ERROR] Запрос к API превысил время ожидания (timeout).")
        return None, "⏰ Время ожидания истекло. Попробуйте позже."

    except requests.exceptions.ConnectionError:
        print("[ERROR] Нет подключения к интернету.")
        return None, "🌐 Нет подключения к интернету."

    except Exception as e:
        print(f"[CRITICAL] Необработанная ошибка: {type(e).__name__}: {e}")
        return None, "🚨 Произошла непредвиденная ошибка."
