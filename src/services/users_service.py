from hashlib import md5
from http import HTTPStatus
from flask import Response

from src.utils.errors import ConflictError, BadRequestError, AccessDeniedError
from src.services.schemas.list_users_filters import ListUsersFilters
from src.security.security import is_authenticated, has_profile

from src.domain.users import Users
from src.infra.repositories.users_repository import UsersRepository
from src.infra.repositories.profiles_repository import ProfilesRepository


class UserService:
    def __init__(self):
        self.repository = UsersRepository()

    def create_user(self, user_data):
        self.__validate_no_default_user(user_data)
        if self.__user_already_exists(user_data['email']):
            ConflictError('There is already a user with this registered email')
        user_data['password'] = self.encode_password(user_data['password'])
        profiles = ProfilesRepository().list_by_name_in(user_data['profiles'])
        user = Users(
            email=user_data['email'],
            password=user_data['password'],
            enable=True
        )
        user.profiles = profiles
        self.repository.create(user)
        return {'id': user.id}

    def __validate_no_default_user(self, user_data):
        profiles = user_data['profiles']
        for profile in profiles:
            if profile not in ['STORE', 'USER'] and not is_authenticated():
                raise AccessDeniedError("you are not allowed to create this type of user")
            if profile in ["ADMIN", "BACKOFFICE"] and not has_profile('ADMIN'):
                raise AccessDeniedError("you are not allowed to create this type of user")
            if profile in ["MANAGER", "TABLE", "WAITER", "KITCHEN", "CASH_OPERATOR"] \
                    and not has_profile("ADMIN", "BACKOFFICE", "STORE"):
                raise AccessDeniedError("you are not allowed to create this type of user")

    def encode_password(self, password: str):
        return md5(password.encode("utf-8")).hexdigest()

    def update_password(self, id, data):
        user: Users = self.read_by_id(id)
        if not self.__check_password(data['old_password'], user):
            raise BadRequestError('old password incorrect')
        self.repository.update_password(user, self.encode_password(data['new_password']))
        return Response(status=HTTPStatus.NO_CONTENT)

    def read_by_id(self, id):
        user = self.repository.read_by_id(id)
        if user is None:
            raise BadRequestError('User Not Found')
        return user

    def list_users(self, filters: ListUsersFilters):
        return self.repository.list_users(filters)

    def update(self, user_id, data_to_update: dict):
        self.repository.update(user_id, data_to_update)

    def update_user_profiles(self, user_id, profiles: dict):
        self.repository.update_profiles(user_id, profiles['profiles'])

    def read_by_email(self, email) -> Users:
        return self.repository.read_by_email(email)

    def __user_already_exists(self, email):
        return self.repository.read_by_email(email) is not None

    def __check_password(self, password, user: Users):
        return user.password == self.encode_password(password)
