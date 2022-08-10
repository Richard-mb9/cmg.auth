from hashlib import md5
from http import HTTPStatus
from flask import Response

from src.utils.errors import ConflictError,BadRequestError, AccessDeniedError
from src.security.security import is_authenticated, has_role, has_profile

from src.domain.models.users import Users
from src.domain.services.profiles_service import ProfilesService
from src.infra.repositories.users_repository import UsersRepository


class UserService:
    def __init__(self):
        self.repository = UsersRepository()

    def create_user(self, user_data):
        self.__validate_no_default_user(user_data)
        if self.__user_already_exists(user_data['email']):
            ConflictError('There is already a user with this registered email')
        user_data = self.encode_password(user_data)
        profile = ProfilesService().read_by_name(user_data['profile'])
        user = Users(
            email=user_data['email'], 
            password=user_data['password'],
            profile_id=profile.id
        )
        self.repository.create(user)
        return {'id': user.id}
    
    def __validate_no_default_user(self, user_data):
        profile = user_data['profile']
        if profile not in ['STORE, USER'] and not is_authenticated():
            raise AccessDeniedError("you are not allowed to create this type of user")
        if profile in ["ADMIN", "BACKOFFICE"] and not has_profile('ADMIN'):
            raise AccessDeniedError("you are not allowed to create this type of user")
        if profile in ["MANAGER", "TABLE", "WAITER", "KITCHEN", "CASH_OPERATOR"] \
        and not has_profile("ADMIN", "BACKOFFICE", "STORE"):
            raise AccessDeniedError("you are not allowed to create this type of user")

        
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


    def __check_password(self, password, user: Users):
        return user.password == self.__encode_md5(password)