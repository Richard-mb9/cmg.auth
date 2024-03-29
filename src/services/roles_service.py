from src.utils.errors import ConflictError, NotFoundError
from src.domain.roles import Roles
from src.domain.profiles import Profiles
from .profiles_service import ProfilesService
from src.infra.repositories.roles_repository import RolesRepository
from src.infra.repositories.profiles_repository import ProfilesRepository


class RolesService:
    def __init__(self):
        self.repository = RolesRepository()
        self.profiles_repository = ProfilesRepository()

    def create_role(self, data):
        if self.__role_already_exists(data['name']):
            ConflictError('there is already a role with this name')
        role = Roles(name=data['name'])
        self.repository.create(role)
        self.__assign_role_to_admin_profile(role.id)
        return {'id': role.id}

    def update_role(self, role_id, data: dict):
        name = data.get('name')
        role = self.read_by_id(role_id)
        if name is not None and name != role.name:
            if self.__role_already_exists(data['name']):
                ConflictError('there is already a role with this name')
            self.repository.update(role_id, {'name': name})

    def delete_role(self, id):
        self.read_by_id(id)
        self.repository.delete(id)

    def list(self, filters: dict = {}):
        return self.repository.list_roles(filters)

    def read_by_id(self, id) -> Roles:
        role = self.repository.read_by_id(id)
        if role is None:
            NotFoundError('role not found')
        return role

    def __role_already_exists(self, name):
        roles = self.repository.read_by_name(name)
        return roles is not None and len(roles) > 0

    def __assign_role_to_admin_profile(self, role_id):
        """assign the new permission to the admin profile"""
        profile = self.profiles_repository.read_by_name('ADMIN')
        if not profile:  # pragma: no cover
            profile = Profiles(name='ADMIN')
            self.profiles_repository.create(profile)
        ProfilesService().assign_to_roles(profile.id, {'roles_ids': [role_id]})
