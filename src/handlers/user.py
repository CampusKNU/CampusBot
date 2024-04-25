from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from src.filters.admin import AdminFilter

from src.database.db_manager import db_session
from src.database.models import MainInfo

from src.keyboards.user import get_main_menu, get_sub_menu

router = Router()


class MultiLevelMenuFSM(StatesGroup):
    menu = State()


@router.message(CommandStart(), ~AdminFilter())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!", parse_mode=ParseMode.HTML, reply_markup=get_main_menu())


@router.message(F.text, ~AdminFilter())
async def command_text_handler(message: Message, state: FSMContext) -> None:
    is_back = False
    split_msg = message.text.split('"')

    if len(split_msg) > 1:
        msg = str(split_msg[1])
        is_back = True
    else:
        msg = message.text

    button = db_session.query(MainInfo).filter_by(title=msg).first()

    if not button:
        await message.answer("Unknown command!")
    else:
        if button.parent_id == -1:
            await state.set_state(MultiLevelMenuFSM.menu)

        await state.update_data(level=button.parent_id)
        await message.answer(button.description, parse_mode=ParseMode.HTML, reply_markup=get_sub_menu(button, is_back))

