from datetime import datetime, timedelta
from sqlalchemy import func
from db_manager import db_session
from .models.log import Log


async def count_logs_this_month(text):
    current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_month_end = (current_month_start.replace(month=current_month_start.month % 12 + 1, day=1) - timedelta(
        days=1)).replace(hour=23, minute=59, second=59)

    count = await db_session.query(func.count(Log.id)).filter(
        Log.text == text,
        Log.to_created >= current_month_start,
        Log.to_created <= current_month_end
    ).scalar()

    return count
