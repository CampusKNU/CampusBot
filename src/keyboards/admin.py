from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Events")],
        [KeyboardButton(text="Main info")],
        [KeyboardButton(text="Admin")]
    ],
        resize_keyboard=True)

    return markup
