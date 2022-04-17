from flask import Response
from http import HTTPStatus

from src.utils.errors import ConflictError, NotFoundError
from src.domain.models.groups import Groups
from src.domain.models.roles import Roles
from src.utils.validator import validator
from src.utils.handlers import object_as_dict

from src.infra.http.groups.validator import insert_group_validator
from src.infra.http.groups.validator import assign_to_rules_validator

class GroupsService:
    def create_group(self, data):
        validator(insert_group_validator, data)
        print("validado")
        if self.__group_already_exists(data['name']):
            ConflictError('there is already a group with this name')
        print("gravando dados")
        try:
            group = Groups(name=data['name']).create()
            return {'id': group.id}
        except Exception as error:
            print(error)
            return {'erro': str(error)}

    
    def list(self):
        groups = Groups().list()
        return object_as_dict(groups)


    def __group_already_exists(self, name):
        groups = Groups().read_by_name(name)
        return groups is not None and len(groups) > 0

    
    def delete(self, id):
        group = self.read_by_id(id)
        group.delete()
    
    def read_by_id(self, id):
        group = Groups().read_by_id(id)
        if group is None:
            NotFoundError('group not found')
        return group

    
    def assign_to_roles(self, group_id, data):
        """must receive a list of role ids, and associate them with the group"""
        validator(assign_to_rules_validator, data)
        roles_ids = data['roles_ids']
        group: Groups = self.read_by_id(group_id)
        roles = Roles().read_by_id_in(roles_ids)
        group.add_roles(roles)
        return Response(status=HTTPStatus.NO_CONTENT)

    
    def unassign_to_roles(self, group_id, data):
        """must receive a list of role ids, and unassociate them with the group"""
        validator(assign_to_rules_validator, data)
        roles_ids = data['roles_ids']
        group: Groups = self.read_by_id(group_id)
        roles = Roles().read_by_id_in(roles_ids)
        group.remove_roles(roles)
        return Response(status=HTTPStatus.NO_CONTENT)

