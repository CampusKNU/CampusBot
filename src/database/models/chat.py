from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP
from .base import BaseModel


class Chat(BaseModel):
    __tablename__ = "Chat"

    topic = Column(String, nullable=False)
    user_name = Column(String, nullable=True)
    status = Column(String, nullable=True)
    to_created = Column(TIMESTAMP, nullable=False)

    def __init__(self, topic, user_name):
        self.topic = topic
        self.user_name = user_name
        self.status = "started"
        self.to_created = datetime.now()
