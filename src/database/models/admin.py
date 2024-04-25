from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP
from .base import BaseModel


class Admin(BaseModel):
    __tablename__ = "Admin"

    user_id = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=True)

    def __init__(self, user_id, role = "default"):
        self.user_id = user_id
        self.role = role
