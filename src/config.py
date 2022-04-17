from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as SessionType
from flask import current_app
from src.utils.getEnv import getEnv


def get_engine(testing: bool):
    host_db = getEnv('host_db') if not testing else None
    password_db = getEnv('password_db') if not testing else None
    user_db = getEnv('user_db') if not testing else None
    database = getEnv('database') if not testing else None
    db_uri = f'postgresql+psycopg2://{user_db}:{password_db}@{host_db}/{database}' \
    if not testing \
    else 'sqlite:///file.db'
    return create_engine(db_uri)
    


def get_session() -> SessionType:
    testing = True
    if current_app:
        testing = current_app.config.get('testing', False)
        if current_app.config.get('session', None):
            return current_app.config['session']
    engine = get_engine(testing)
    Session = sessionmaker(autocommit=False,autoflush=False, bind=engine)
    session: SessionType = Session()
    if current_app:
        current_app.config['session'] = session
    return session


Base = declarative_base()


