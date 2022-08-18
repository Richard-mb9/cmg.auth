from src.config import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship

user_profiles = Table('user_profiles', Base.metadata,
    Column('profile_id', Integer, ForeignKey('profiles.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    enable = Column(Boolean, default=True)
    profiles = relationship('Profiles', secondary=user_profiles)

    def __repr__(self): # pragma: no cover
        return f'User {self.email}'



