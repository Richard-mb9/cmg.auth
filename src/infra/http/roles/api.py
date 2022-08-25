from flask import Blueprint
from flask import request, Response
from json import loads
from http import HTTPStatus
from flask import jsonify

from src.security.security import roles_allowed
from src.services.roles_service import RolesService
from src.utils.validator import validator
from src.utils.handlers import get_items_to_querys_from_request
from .validator import insert_rule_validator
from .validator import update_rule_validator
from .validator import filter_roles_validator

service = RolesService()

app = Blueprint('roles', __name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
@roles_allowed('CREATE_ROLES')
def create_rule():
    data = loads(request.data)
    validator(insert_rule_validator, data)
    return jsonify(service.create_role(data)), HTTPStatus.CREATED


@app.route('', methods=['GET'])
@roles_allowed('READ_ROLES', 'CREATE_ROLES')
def list_roles():
    filters = get_items_to_querys_from_request()
    validator(filter_roles_validator, filters)
    return jsonify(service.list(filters))


@app.route('/<rule_id>', methods=['PUT'])
@roles_allowed('UPDATE_ROLES')
def update_rule(rule_id):
    data = loads(request.data)
    validator(update_rule_validator, data)
    service.update_role(rule_id, data)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/<rule_id>', methods=['DELETE'])
@roles_allowed('DELETE_ROLES')
def delete_role(rule_id):
    service.delete_role(rule_id)
    return Response(status=HTTPStatus.NO_CONTENT)
