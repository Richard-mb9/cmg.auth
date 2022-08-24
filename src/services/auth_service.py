from datetime import datetime
from typing import List
from src.utils.handlers import object_as_dict
from src.utils.errors import BadRequestError, AccessDeniedError
from src.security.Auth import Auth
from src.services.schemas.auth_request_schema import AuthRequest

from src.services.users_service import UserService
from src.domain.users import Users
from src.domain.profiles import Profiles


class AuthService:
    def login(self, data: AuthRequest):
        user: Users = UserService().read_by_email(data['email'])
        if user and user.attempts and user.attempts >= 5 \
                and self.get_interval_last_tryed_invalid(user.last_try_invalid) <= 10:
            raise AccessDeniedError("user blocked due to too many failed attempts")

        if not user:
            raise BadRequestError("incorrect credentials")
        else:
            user_password = user.password
            data_password = UserService().encode_password(data.get('password', ''))
            if user.enable is False:
                raise BadRequestError("incorrect credentials")
            elif user_password != data_password:
                attempts = user.attempts if user.attempts else 0
                self.__update_attempts(user.id, (attempts + 1))
                raise BadRequestError("incorrect credentials")
        self.__update_attempts(user.id, clear=True)
        profiles = user.profiles
        roles = self.get_roles(profiles)
        profiles_names = [profile.name for profile in profiles]
        token_data = {
            'id': user.id,
            'email': user.email,
            'roles': roles,
            'profile': profiles_names
        }
        return {
            'access_token': Auth().generateToken(token_data),
            'token_type': 'Bearer'
        }

    def get_roles(self, profiles: List[Profiles]):
        roles = set()
        for profile in profiles:
            roles_in_profile = object_as_dict(profile.roles)
            for role in roles_in_profile:
                roles.add(role['name'])
        return list(roles)

    def get_interval_last_tryed_invalid(self, time: datetime):
        now = datetime.now()
        return ((now - time).seconds) / 60

    def __update_attempts(self, user_id, attempts=0, clear=None):
        UserService().update(user_id, {
            'attempts': attempts,
            'last_try_invalid': datetime.now() if not clear else None
        })
