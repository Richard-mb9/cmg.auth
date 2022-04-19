from flask import Blueprint
from flask import request, Response
from json import dumps, loads
from http import HTTPStatus
from flask import jsonify

from src.security.security import login_required, roles_allowed
from src.modules.auth.domain.services.roles_service import RolesService
from src.utils.validator import validator
from .validator import insert_rule_validator

service = RolesService()

app = Blueprint('roles',__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
@roles_allowed('create roles')
def create_rule():
    data = loads(request.data)
    validator(insert_rule_validator, data)
    return jsonify(service.create_role(data)), HTTPStatus.CREATED


@app.route('', methods=['GET'])
@login_required
def list_roles():
    return jsonify(service.list())


@app.route('/<rule_id>', methods=['DELETE'])
@roles_allowed('delete roles')
def delete_role(rule_id):
    service.delete_role(rule_id)
    return Response(status=HTTPStatus.NO_CONTENT)