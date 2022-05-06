from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as SessionType
from flask import current_app
from decouple import config
from distutils.util import strtobool


def is_testing():
    return bool(strtobool(config('testing', default='False')))


def get_engine():
    testing = is_testing()
    host_db = config('host_db', default=None) if not testing else None
    password_db = config('password_db', default=None) if not testing else None
    user_db = config('user_db', default=None) if not testing else None
    database = config('database', default=None) if not testing else None
    db_uri = f'postgresql+psycopg2://{user_db}:{password_db}@{host_db}/{database}' \
    if not testing \
    else 'sqlite:///file.db'
    return create_engine(db_uri)
    

def get_session() -> SessionType:
    if current_app:
        if current_app.config.get('session', None):
            return current_app.config['session']
    engine = get_engine()
    Session = sessionmaker(autocommit=False,autoflush=False, bind=engine)
    session: SessionType = Session()
    if current_app:
        current_app.config['session'] = session
    return session


Base = declarative_base()


