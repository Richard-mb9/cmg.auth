from src.utils.errors import ConflictError, NotFoundError
from src.domain.models.roles import Roles
from src.domain.models.groups import Groups
from src.utils.handlers import object_as_dict
from .groups_service import GroupsService

class RolesService:
    def create_role(self, data):
        if self.__role_already_exists(data['name']):
            ConflictError('there is already a role with this name')
        role = Roles(name=data['name']).create()
        self.__assign_role_to_admin_group(role.id)
        return {'id': role.id}


    def delete_role(self, id):
        role = self.read_by_id(id)
        role.delete()
            

    def list(self):
        roles = Roles().list()
        return object_as_dict(roles)

    def read_by_id(self, id):
        role = Roles().read_by_id(id)
        if role is None:
            NotFoundError('role not found')
        return role


    def __role_already_exists(self, name):
        roles = Roles().read_by_name(name)
        return roles is not None and len(roles) > 0

    
    def __assign_role_to_admin_group(self, role_id):
        """assign the new permission to the admin group"""
        group = Groups().read_by_name('admin')
        if not group:
            group = Groups(name='admin').create()
        GroupsService().assign_to_roles(group.id, {'roles_ids': [role_id]})