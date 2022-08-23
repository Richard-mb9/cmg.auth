from src.config import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


profiles_roles = Table('profiles_roles', Base.metadata,
    Column('profile_id', Integer,ForeignKey('profiles.id')),
    Column('role_id', Integer,ForeignKey('roles.id'))
)


class Profiles(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    roles = relationship('Roles', secondary=profiles_roles)
    
    def __repr__(self): # pragma: no cover
        return f'Profile {self.name}'