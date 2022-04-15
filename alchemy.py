from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from os import getenv

Base = declarative_base()
engine = create_engine(getenv('TOKEN'))
Session = sessionmaker()
