from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup


def get_start_menu_button() -> ReplyKeyboardMarkup:
    """

    Клавиатура для главного меню бота

    Returns:
        ReplyKeyboardMarkup: Возвращает reply клавиатуру
    """

    reply_kb: ReplyKeyboardBuilder = ReplyKeyboardBuilder(
        [
            [
                KeyboardButton(text="Описание Изображений"),
            ],
            [
                KeyboardButton(text="Генерация Изображений"),
            ],
            [
                KeyboardButton(text="Генерация Видео"),
            ],
        ]
    )

    return reply_kb.as_markup(resize_keyboard=True)
