from datetime import datetime

from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Message(BaseModel):
    __tablename__ = "Message"

    text = Column(String, nullable=False)
    sender_id = Column(String, nullable=False)
    chat_id = Column(String, ForeignKey("Chat.id"))
    to_created = Column(TIMESTAMP, nullable=False)

    # virtual property
    chat = relationship('Chat', foreign_keys='Message.chat_id')

    def __init__(self, text, sender_id, chat_id):
        self.text = text
        self.sender_id = sender_id
        self.chat_id = chat_id
        self.to_created = datetime.now()
