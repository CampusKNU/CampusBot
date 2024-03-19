from datetime import datetime
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database

from .models import BaseModel

# default for sqlite: sqlite:///test-database.db
engine = create_engine(getenv('CON_STRING'))
if not database_exists(engine.url):
    create_database(engine.url)

BaseModel.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db_session = Session()
