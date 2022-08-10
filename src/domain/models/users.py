from src.config import Base

from sqlalchemy import Column, Integer, String, ForeignKey

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)

    def __repr__(self): # pragma: no cover
        return f'User {self.email}'



