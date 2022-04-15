from src.data.baseModel.baseModel import BaseModel
from src.config import Base, get_session

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


users_groups = Table('users_groups', Base.metadata,
    Column('user_id', Integer,ForeignKey('users.id')),
    Column('group_id', Integer,ForeignKey('groups.id'))
)

class Users(Base ,BaseModel):
    __tablename__ = 'users'

    email = Column(String)
    password = Column(String)
    groups = relationship('Groups', secondary=users_groups)


    def add_groups(self, groups: list):
        session = get_session()
        for group in groups:
            self.groups.append(group)
        session.commit()

    def remove_groups(self, groups: list):
        session = get_session()
        new_groups = []
        for group in self.groups:
            if group not in groups:
                new_groups.append(group)
        self.groups = new_groups
        session.commit()

    def update_password(self, password):
        self.password = password
        return self

    def read_by_email(self, email):
        session = get_session()
        return session.query(Users).filter_by(email=email).all()

    def __repr__(self):
        return f'User {self.email}'



