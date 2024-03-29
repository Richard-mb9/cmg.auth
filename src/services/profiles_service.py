from flask import Response
from http import HTTPStatus

from src.utils.errors import ConflictError, NotFoundError
from src.domain.profiles import Profiles
from src.infra.repositories.profiles_repository import ProfilesRepository
from src.infra.repositories.roles_repository import RolesRepository
from src import services
from src.utils.handlers import object_as_dict


class ProfilesService:
    def __init__(self):
        self.repository = ProfilesRepository()
        self.roles_repository = RolesRepository()
        self.roles_service = services.roles_service.RolesService()

    def create_profile(self, data):
        if self.__profile_already_exists(data['name']):
            ConflictError('there is already a profile with this name')
        role_id = None
        if data.get('role_name') is not None:
            role_id = self.roles_service.create_role({'name': data['role_name']})['id']
        profile = Profiles(name=data['name'], role_id=role_id)
        self.repository.create(profile)
        return {'id': profile.id}

    def list(self, filters: dict = {}):
        return self.repository.list_profiles(filters)

    def __profile_already_exists(self, name):
        profile = self.read_by_name(name)
        return profile is not None

    def read_by_name(self, profile_name: str) -> Profiles:
        return self.repository.read_by_name(profile_name)

    def delete(self, id):
        self.read_by_id(id)
        self.repository.delete(id)

    def read_by_id(self, id: int, raise_not_found=True) -> Profiles:
        profile = self.repository.read_by_id(id)
        if profile is None and raise_not_found:
            NotFoundError('profile not found')
        return profile

    def list_roles_from_profiles(self, profile_id: int):
        profile = self.read_by_id(profile_id)
        return object_as_dict(profile.roles)

    def update_profile(self, profile_id: int, data_to_update: dict):
        profile = self.read_by_id(profile_id)
        roles_ids = data_to_update.get('roles_ids')
        profile_name = data_to_update.get('name')
        if profile_name and profile_name != profile.name:
            if self.__profile_already_exists(profile_name):
                ConflictError('there is already a profile with this name')
            self.repository.update(profile_id, {'name': profile_name})
        if roles_ids:
            roles = self.roles_repository.read_by_id_in(roles_ids)
            self.repository.update_roles(profile, roles)

    def assign_to_roles(self, profile_id, data):
        """must receive a list of role ids, and associate them with the profile"""
        roles_ids = data['roles_ids']
        profile: Profiles = self.read_by_id(profile_id)
        roles = self.roles_repository.read_by_id_in(roles_ids)
        self.repository.add_roles(profile, roles)
        return Response(status=HTTPStatus.NO_CONTENT)
