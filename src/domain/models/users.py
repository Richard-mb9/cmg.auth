from src.data.baseModel.baseModel import BaseModel
from config import Base, get_session

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

#session = get_session()

users_roles = Table('users_roles', Base.metadata,
    Column('user_id', Integer,ForeignKey('users.id')),
    Column('role_id', Integer,ForeignKey('roles.id'))
)

class Users(Base ,BaseModel):
    __tablename__ = 'users'

    email = Column(String)
    password = Column(String)
    roles = relationship('Roles', secondary=users_roles)


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

    def update_password(self, password):
        self.password = password
        return self

    def read_by_email(self, email):
        session = get_session()
        return session.query(Users).filter_by(email=email).all()

    def __repr__(self):
        return f'User {self.email}'



