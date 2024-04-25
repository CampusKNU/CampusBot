from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.database.db_manager import db_session
from src.database.models import MainInfo


def get_main_menu() -> ReplyKeyboardMarkup:
    buttons = db_session.query(MainInfo).filter_by(parent_id=-1).all()

    builder = ReplyKeyboardBuilder()

    for bt in buttons:
        builder.add(KeyboardButton(text=bt.title))

    builder.adjust(2)

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup


def get_sub_menu(button: MainInfo, is_back: bool):
    # if action is back, show PREVIOUS keyboard
    # if simply click common button, show NEXT keyboard
    if is_back:
        searched_id = button.parent_id
    else:
        searched_id = button.id

    buttons = db_session.query(MainInfo).filter_by(parent_id=searched_id).all()

    # if pressed button has no children, return None
    if len(buttons) == 0:
        return None

    builder = ReplyKeyboardBuilder()

    for bt in buttons:
        builder.add(KeyboardButton(text=bt.title))

    builder.adjust(2)

    # do not show `back` button, if keyboard is main
    if searched_id != -1:
        parent_btn = db_session.query(MainInfo).filter_by(id=buttons[0].parent_id).first()
        builder.row(KeyboardButton(text=f'↩️ Назад до "{parent_btn.title}"'))

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup
