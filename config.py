from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as SessionType
from flask import current_app


def get_engine(testing):
    db_uri = 'postgresql+psycopg2://login:login@localhost/cmg_db' \
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


