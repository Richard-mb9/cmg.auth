from src.utils.errors import ConflictError, NotFoundError
from src.domain.models.roles import Roles
from src.domain.models.groups import Groups
from src.utils.handlers import object_as_dict
from .groups_service import GroupsService
from src.infra.repositories.roles_repository import RolesRepository
from src.infra.repositories.groups_repository import GroupsRepository


class RolesService:
    def __init__(self):
        self.repository = RolesRepository(Roles)
        self.groups_repository = GroupsRepository(Groups)

    def create_role(self, data):
        if self.__role_already_exists(data['name']):
            ConflictError('there is already a role with this name')
        role = Roles(name=data['name'])
        self.repository.create(role)
        self.__assign_role_to_admin_group(role.id)
        return {'id': role.id}


    def delete_role(self, id):
        self.read_by_id(id)
        self.repository.delete(id)
            

    def list(self):
        roles = self.repository.list()
        return object_as_dict(roles)

    def read_by_id(self, id):
        role = self.repository.read_by_id(id)
        if role is None:
            NotFoundError('role not found')
        return role


    def __role_already_exists(self, name):
        roles = self.repository.read_by_name(name)
        return roles is not None and len(roles) > 0

    
    def __assign_role_to_admin_group(self, role_id):
        """assign the new permission to the admin group"""
        group = self.groups_repository.read_by_name('admin')
        if not group:
            group = Groups(name='admin')
            self.groups_repository.create(group)
        GroupsService().assign_to_roles(group.id, {'roles_ids': [role_id]})