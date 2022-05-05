from src.config import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


groups_roles = Table('groups_roles', Base.metadata,
    Column('group_id', Integer,ForeignKey('groups.id')),
    Column('role_id', Integer,ForeignKey('roles.id'))
)


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    roles = relationship('Roles', secondary=groups_roles)
    
    def __repr__(self): # pragma: no cover
        return f'Group {self.name}'