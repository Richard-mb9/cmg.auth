from src.data.baseModel.baseModel import BaseModel
from src.config import Base, get_session

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


groups_roles = Table('groups_roles', Base.metadata,
    Column('group_id', Integer,ForeignKey('groups.id')),
    Column('role_id', Integer,ForeignKey('roles.id'))
)


class Groups(Base ,BaseModel):
    __tablename__ = 'groups'

    name = Column(String)
    roles = relationship('Roles', secondary=groups_roles)

    def read_by_name(self, name):
        print("criando seção")
        session = get_session()
        try:
            print("proucurando grupo")
            return session.query(Groups).filter_by(name=name).all()
        except Exception as error:
            print('ocorreu um erro')
            print(error)
            return None


    def add_roles(self, roles: list):
        session = get_session()
        for role in roles:
            self.roles.append(role)
        session.commit()

    def remove_roles(self, roles: list):
        session = get_session()
        new_roles = []
        for role in self.roles:
            if role not in roles:
                new_roles.append(role)
        self.roles = new_roles
        session.commit()

    
    def __repr__(self):
        return f'Group {self.name}'