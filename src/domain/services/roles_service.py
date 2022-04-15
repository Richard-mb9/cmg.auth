from src.utils.errors import ConflictError, NotFoundError
from src.config import get_session
from src.domain.models.roles import Roles
from src.utils.validator import validator
from src.utils.handlers import object_as_dict

from src.infra.http.roles.validator import insert_rule_validator

class RolesService:
    def create_role(self, data):
        validator(insert_rule_validator, data)
        if self.__role_already_exists(data['name']):
            ConflictError('there is already a role with this name')
        role = Roles(name=data['name']).create()
        return {'id': role.id}


    def delete_role(self, id):
        role = self.read_by_id(id)
        role.delete()
            

    def list(self):
        roles = Roles().list()
        return object_as_dict(roles)

    def __role_already_exists(self, name):
        roles = Roles().read_by_name(name)
        return roles is not None and len(roles) > 0

    
    def read_by_id(self, id):
        role = Roles().read_by_id(id)
        if role is None:
            NotFoundError('role not found')
        return role
