from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode

from src.filters.admin import AdminFilter
from src.database.db_manager import db_session

from src.keyboards.admin import get_main_menu

router = Router()


@router.message(CommandStart(), AdminFilter())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello admin, {message.from_user.full_name}!", parse_mode=ParseMode.HTML,
                         reply_markup=get_main_menu())
