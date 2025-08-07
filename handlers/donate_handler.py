# handlers/donate_handler.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from keyboards.donate_keyboard import donate_kb

router = Router()

# Путь к вашему QR-коду
QR_PATH = "assets/QR_code.jpg"


@router.message(Command("donate"))
async def cmd_donate(message: Message):
    """Отправляет пользователю QR-код и две кнопки для доната"""
    # Отправляем текст с кнопками
    await message.answer(
        "Вы можете поддержать развитие бота 💖\n\n"
        "Это поможет оставить бота бесплатным и улучшать его.\n\n"
        "Выберите удобный способ:",
        reply_markup=donate_kb
    )

    # Отправляем QR-код как фото
    try:
        photo = FSInputFile(QR_PATH)
        await message.answer_photo(
            photo=photo,
            caption="💳 Отсканируйте QR-код в своём банке\n"
                    "Перевод по СБП — без комиссии!"
        )
    except FileNotFoundError:
        await message.answer(
            "❌ QR-код временно недоступен.\n"
            "Попробуйте [перейти по ссылке](https://www.tinkoff.ru/rm/r_uadSYUBdzf.GfKeMjixpq/UZwqb94862)",
            parse_mode="Markdown"
        )


@router.callback_query(F.data == "download_qr")
async def download_qr(callback: CallbackQuery):
    """Отправляет QR-код как документ для скачивания"""
    # Отвечаем на callback, чтобы убрать "часики"
    await callback.answer()

    try:
        document = FSInputFile(QR_PATH)
        await callback.message.answer_document(
            document=document,
            caption="📎 Вот ваш QR-код. Сохраните и откройте в приложении банка."
        )
    except FileNotFoundError:
        if callback.message:
            await callback.message.answer("❌ Файл QR-кода не найден. Обратитесь к разработчику.")
        else:
            # Если message отсутствует — отправляем в чат через bot
            bot = callback.bot
            await bot.send_message(callback.from_user.id, "❌ Файл QR-кода не найден.")


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    """Кнопка 'Назад' — удаляет или редактирует сообщение"""
    await callback.answer()  # убираем "часики"

    if callback.message:
        try:
            # Пытаемся отредактировать сообщение
            await callback.message.edit_text(
                "Выбери город из списка или введи любой город вручную.",
                reply_markup=None  # убираем клавиатуру
            )
        except Exception as e:
            # Если нельзя редактировать (например, старое сообщение), просто отправляем новое
            await callback.message.answer("Выбери город из списка или введи любой город вручную.")
    else:
        # Если message нет — отправляем в личку через bot
        await callback.bot.send_message(callback.from_user.id, "Выбери город из списка или введи любой город вручную.")