from dotenv import find_dotenv, load_dotenv

from src.config import Base, get_engine
from src.app import app

env = find_dotenv('.env.local')
load_dotenv(env)
Base.metadata.create_all(bind=get_engine())
