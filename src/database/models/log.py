from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .base import BaseModel

class Log(BaseModel):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    user_id = Column(Integer)
    to_created = Column(DateTime, default=datetime.utcnow)

    def __init__(self, text, user_id, to_created=None):
        self.text = text
        self.user_id = user_id
        if to_created is None:
            self.to_created = datetime.now()
        else:
            self.to_created = to_created
