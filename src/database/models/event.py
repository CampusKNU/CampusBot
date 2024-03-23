from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP, DateTime
from .base import BaseModel


class Event(BaseModel):
    __tablename__ = "Event"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    link = Column(String, nullable=True)
    photo_id = Column(String, nullable=True)
    status = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)
    to_created = Column(TIMESTAMP, nullable=False)

    def __init__(self, title, description, link, date):
        self.title = title
        self.description = description
        self.link = link
        self.photo_id = -1
        self.status = "announced"
        self.date = date
        self.to_created = datetime.now()
