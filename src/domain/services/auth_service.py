from src.utils.handlers import object_as_dict
from src.utils.errors import BadRequestError
from src.security.Auth import Auth

from src.domain.services.users_service import UserService
from src.domain.models.users import Users

class AuthService:
    def login(self, data):
        user = UserService().read_by_email_and_password(data['email'], data['password'])
        if not user:
            raise BadRequestError("incorrect credentials")
        groups = self.get_groups(user)
        roles = self.get_roles(groups)
        token_data = {
            'id': user.id,
            'email': user.email,
            'roles': roles,
            'profile': user.profile
        }
        return {'token': Auth().generateToken(token_data)}


    def get_groups(self ,user: Users):
        groups = user.groups
        return groups


    def get_roles(self, groups: list):
        roles = set()
        for group in groups:
            roles_in_group = object_as_dict(group.roles)
            for role in roles_in_group:
                roles.add(role['name'])
        return list(roles)

        