from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as SessionType
from flask import current_app
from decouple import config
from distutils.util import strtobool
from dotenv import load_dotenv, find_dotenv


def is_testing():
    return bool(strtobool(config('testing', default='False')))


def get_db_url():
    if is_testing():
        env = find_dotenv('.env.test')
        load_dotenv(env)
    else:
        env = find_dotenv('.env.local')
        load_dotenv(env)
    host_db = config('HOST_DB', default=None)
    password_db = config('PASSWORD_DB', default=None)
    user_db = config('USER_DB', default=None)
    database = config('NAME_DB', default=None)
    port_db = int(config('PORT_DB', default=None))
    return f'postgresql+psycopg2://{user_db}:{password_db}@{host_db}:{port_db}/{database}'


def get_engine():
    url_db = get_db_url()
    print(url_db)
    return create_engine(url_db)


def get_session() -> SessionType:
    if current_app:
        if current_app.config.get('session', None):
            return current_app.config['session']
    engine = get_engine()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session: SessionType = Session()
    if current_app:
        current_app.config['session'] = session
    return session


Base = declarative_base()
