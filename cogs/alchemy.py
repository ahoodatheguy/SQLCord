from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base


from os import getenv

engine = create_engine(getenv('TOKEN'))
Session = sessionmaker()

Base = automap_base()
Base.prepare(engine, reflect=True)
