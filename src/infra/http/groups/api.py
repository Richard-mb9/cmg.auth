from flask import Blueprint
from flask import request, Response
from json import dumps, loads
from http import HTTPStatus
from flask import jsonify

from src.domain.services.groups_service import GroupsService

service = GroupsService()

app = Blueprint('groups',__name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
def create_group():
    data = loads(request.data)
    return Response(dumps(service.create_group(data)), status=HTTPStatus.CREATED)


@app.route('', methods=['GET'])
def list_groups():
    return jsonify(service.list())


@app.route('/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    service.delete(group_id)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/<group_id>/roles/assign', methods=['POST'])
def assign_to_roles(group_id):
    data = loads(request.data)
    return service.assign_to_roles(group_id ,data)


@app.route('/<group_id>/roles/unassign', methods=['POST'])
def unassign_to_roles(group_id):
    data = loads(request.data)
    return service.unassign_to_roles(group_id ,data)

