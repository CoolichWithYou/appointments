from server.schema import Appointment

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from server.settings import Settings

settings = Settings()

engine = create_engine(settings.get_connection())
