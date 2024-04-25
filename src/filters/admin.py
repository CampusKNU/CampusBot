from aiogram.filters import Filter
from aiogram.types import Message

from src.database.db_manager import db_session
from src.database.models import Admin


class AdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        admin = db_session.query(Admin).filter_by(user_id=message.from_user.id).first()

        return admin is not None
