from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

donate_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Открыть QR-код",
                callback_data="download_qr"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔗 Открыть страницу для перевода",
                url="https://www.tinkoff.ru/rm/r_uadSYUBdzf.GfKeMjixpq/UZwqb94862"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="back_to_menu"
            )
        ],
    ]
)