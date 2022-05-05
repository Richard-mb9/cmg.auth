from flask import Response
from http import HTTPStatus

from src.utils.errors import ConflictError, NotFoundError
from src.domain.models.groups import Groups
from src.domain.models.roles import Roles
from src.infra.repositories.groups_repository import GroupsRepository
from src.infra.repositories.roles_repository import RolesRepository
from src.utils.handlers import object_as_dict

class GroupsService:
    def __init__(self):
        self.repository = GroupsRepository(Groups)
        self.roles_repository = RolesRepository(Roles)

    def create_group(self, data):
        if self.__group_already_exists(data['name']):
            ConflictError('there is already a group with this name')
        group = Groups(name=data['name'])
        self.repository.create(group)
        return {'id': group.id}

    
    def list(self):
        groups = self.repository.list()
        return object_as_dict(groups)


    def __group_already_exists(self, name):
        groups = self.repository.read_by_name(name)
        return groups is not None

    
    def delete(self, id):
        self.read_by_id(id)
        self.repository.delete(id)
    
    def read_by_id(self, id):
        group = self.repository.read_by_id(id)
        if group is None:
            NotFoundError('group not found')
        return group

    
    def assign_to_roles(self, group_id, data):
        """must receive a list of role ids, and associate them with the group"""
        roles_ids = data['roles_ids']
        group: Groups = self.read_by_id(group_id)
        roles = self.roles_repository.read_by_id_in(roles_ids)
        self.repository.add_roles(group, roles)
        return Response(status=HTTPStatus.NO_CONTENT)

    
    def unassign_to_roles(self, group_id, data):
        """must receive a list of role ids, and unassociate them with the group"""
        roles_ids = data['roles_ids']
        group: Groups = self.read_by_id(group_id)
        roles = self.roles_repository.read_by_id_in(roles_ids)
        self.repository.remove_roles(group, roles)
        return Response(status=HTTPStatus.NO_CONTENT)

