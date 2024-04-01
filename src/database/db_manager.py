from datetime import datetime
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm.exc import NoResultFound

from .models import BaseModel, Event

# default for sqlite: sqlite:///test-database.db
engine = create_engine(getenv('CON_STRING'))
if not database_exists(engine.url):
    create_database(engine.url)

BaseModel.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db_session = Session()


def get_events():
    """
    Retrieve all events from the database.
    """
    return db_session.query(Event).all()

def get_event_by_id(event_id):
    """
    Retrieve an event from the database by its ID.
    :param event_id: The ID of the event to retrieve.
    :return: The event object if found, None otherwise.
    """
    try:
        return db_session.query(Event).filter(Event.id == event_id).one()
    except NoResultFound:
        return None


def save_event(data):
    """
    Add a new event to the database.
    """
    title = data["title"]
    description = data["description"]
    link = data["link"]
    photo_id = data["photo_id"]
    status = data["status"]
    date = data["date"]
    new_event = Event(title=title, description=description, link=link, date=date, photo_id=photo_id, status=status)
    db_session.add(new_event)
    db_session.commit()
    return new_event


def update_event(event_id, **kwargs):
    """
    Update an existing event in the database.
    """
    event = db_session.query(Event).filter(Event.id == event_id).first()
    if event:
        for key, value in kwargs.items():
            setattr(event, key, value)
        db_session.commit()
        return event
    else:
        return None


def delete_event(event_id):
    """
    Delete an event from the database.
    """
    event = db_session.query(Event).filter(Event.id == event_id).first()
    if event:
        db_session.delete(event)
        db_session.commit()
        return True
    else:
        return False