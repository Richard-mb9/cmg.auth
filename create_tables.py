from src.config import Base, get_engine
from src.app import app

Base.metadata.create_all(bind=get_engine(False))
