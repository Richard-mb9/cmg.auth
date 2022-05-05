from hashlib import md5
from http import HTTPStatus
from json import dumps
from pickletools import read_uint1
from flask import Response

from src.utils.errors import ConflictError,BadRequestError

from src.domain.models.users import Users
from src.domain.models.groups import Groups
from src.infra.repositories.users_repository import UsersRepository
from src.infra.repositories.groups_repository import GroupsRepository


class UserService:
    def __init__(self):
        self.repository = UsersRepository(Users)
        self.groups_repository = GroupsRepository(Groups)

    def create_user(self, user_data):
        if self.__user_already_exists(user_data['email']):
            ConflictError('There is already a user with this registered email')
        user_data = self.encode_password(user_data)
        user = Users(
            email=user_data['email'], 
            password=user_data['password'], 
            profile=user_data['profile']
        )
        self.repository.create(user)
        return dumps({'id': user.id})

        
    def encode_password(self, user_data):
        password = user_data['password']
        user_data['password'] = self.__encode_md5(password)
        return user_data


    def update_password(self, id, data):
        user: Users = self.read_by_id(id)
        if not self.__check_password(data['old_password'], user):
            BadRequestError('old password incorrect')
        self.repository.update_password(user, self.__encode_md5(data['new_password']))
        return Response(status=HTTPStatus.NO_CONTENT)


    def read_by_id(self, id):
        user = self.repository.read_by_id(id)
        if user is None:
            BadRequestError('User Not Found')
        return user


    def read_by_email_and_password(self, email, password) -> Users:
        return self.repository.read_by_email_and_password(email, self.__encode_md5(password))
        

    def __encode_md5(self, data:str):
        return md5(data.encode("utf-8")).hexdigest()

    
    def __user_already_exists(self, email):
        return len(self.repository.read_by_email(email)) > 0


    def __check_password(self, password, user):
        return user.password == self.__encode_md5(password)


    def assign_to_groups(self, user_id, data):
        """must receive a list of group ids, and associate them with the user"""
        groups_ids = data['groups_ids']
        user: Users = self.read_by_id(user_id)
        groups = self.groups_repository.read_by_id_in(groups_ids)
        self.repository.add_groups(user, groups)
        return Response(status=HTTPStatus.NO_CONTENT)


    def unassign_to_groups(self, user_id, data):
        """must receive a list of group ids, and remove to user"""
        groups_ids = data['groups_ids']
        user: Users = self.read_by_id(user_id)
        groups = self.groups_repository.read_by_id_in(groups_ids)
        self.repository.remove_groups(user, groups)
        return Response(status=HTTPStatus.NO_CONTENT)