from src.data.baseModel.baseModel import BaseModel
from src.config import Base, get_session

from sqlalchemy import Column, Integer, String

class Roles(Base, BaseModel):
    __tablename__ = 'roles'

    name = Column(String)

    def read_by_name(self, name):
        session = get_session()
        return session.query(Roles).filter_by(name=name).all()

    def __repr__(self):
        return f'Role {self.name}'

