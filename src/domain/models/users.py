from src.config import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


users_groups = Table('users_groups', Base.metadata,
    Column('user_id', Integer,ForeignKey('users.id')),
    Column('group_id', Integer,ForeignKey('groups.id'))
)

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    profile = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    groups = relationship('Groups', secondary=users_groups)

    def __repr__(self): # pragma: no cover
        return f'User {self.email}'



