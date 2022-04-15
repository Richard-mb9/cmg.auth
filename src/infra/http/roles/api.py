from flask import Blueprint
from flask import request, Response
from json import dumps, loads
from http import HTTPStatus
from flask import jsonify

from ....domain.services.roles_service import RolesService

service = RolesService()

app = Blueprint('roles',__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@app.route('', methods=['POST'])
def create_rule():
    data = loads(request.data)
    return Response(dumps(service.create_role(data)), status=HTTPStatus.CREATED)


@app.route('', methods=['GET'])
def list_roles():
    return jsonify(service.list())


@app.route('/<rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    service.delete_role(rule_id)
    return Response(status=HTTPStatus.NO_CONTENT)