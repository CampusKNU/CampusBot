from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP
from .base import BaseModel


class MainInfo(BaseModel):
    __tablename__ = "MainInfo"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    link = Column(String, nullable=True)
    # id of parent button (MainInfo object)
    parent_id = Column(Integer, nullable=True)
    to_updated = Column(TIMESTAMP, nullable=False)

    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link
        self.parent_id = -1
        self.to_updated = datetime.now()
