from src.config import Base

from sqlalchemy import Column, Integer, String

class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self): # pragma: no cover
        return f'Role {self.name}'

