from typing import List
from src.utils.handlers import object_as_dict
from src.utils.errors import BadRequestError
from src.security.Auth import Auth

from src.domain.services.users_service import UserService
from src.domain.services.profiles_service import ProfilesService
from src.domain.models.users import Users
from src.domain.models.profiles import Profiles

class AuthService:
    def login(self, data):
        user: Users = UserService().read_by_email_and_password(data['email'], data['password'])
        if not user:
            raise BadRequestError("incorrect credentials")
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

        