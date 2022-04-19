from flask import Blueprint
from flask import request, Response
from json import dumps, loads
from http import HTTPStatus
from flask import jsonify

from src.modules.auth.domain.services.groups_service import GroupsService
from src.security.security import login_required, roles_allowed
from src.utils.validator import validator
from .validator import assign_to_rules_validator
from .validator import insert_group_validator

service = GroupsService()

app = Blueprint('groups',__name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
@roles_allowed('create groups')
def create_group():
    data = loads(request.data)
    validator(insert_group_validator, data)
    return jsonify(service.create_group(data)), HTTPStatus.CREATED


@app.route('', methods=['GET'])
@login_required
def list_groups():
    return jsonify(service.list())


@app.route('/<group_id>', methods=['DELETE'])
@roles_allowed('delete groups')
def delete_group(group_id):
    service.delete(group_id)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/<group_id>/roles/assign', methods=['POST'])
@roles_allowed('groups management')
def assign_to_roles(group_id):
    data = loads(request.data)
    validator(assign_to_rules_validator, data)
    return service.assign_to_roles(group_id ,data)


@app.route('/<group_id>/roles/unassign', methods=['POST'])
@roles_allowed('groups management')
def unassign_to_roles(group_id):
    data = loads(request.data)
    validator(assign_to_rules_validator, data)
    return service.unassign_to_roles(group_id ,data)

