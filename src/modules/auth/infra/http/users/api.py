from http import HTTPStatus
from flask import Blueprint
from flask import request, Response
from json import loads

from src.security.security import login_required, roles_allowed
from src.modules.auth.domain.services.users_service import UserService
from src.utils.validator import validator
from .validators import insert_user_validator
from .validators import update_password_validator
from .validators import assign_to_groups_validator

service = UserService()

app = Blueprint('users',__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
def insert_user():
    user_data = loads(request.data)
    validator(insert_user_validator, user_data)
    return Response(service.create_user(user_data), status=HTTPStatus.CREATED)


@app.route('/<user_id>/update-password', methods=['PUT'])
@login_required
def update_password(user_id):
    data = loads(request.data)
    validator(update_password_validator, data)
    return service.update_password(user_id ,data)


@app.route('/<user_id>/groups/assign', methods=['POST'])
@roles_allowed('user management')
def assign_to_groups(user_id):
    data = loads(request.data)
    validator(assign_to_groups_validator, data)
    return service.assign_to_groups(user_id ,data)


@app.route('/<user_id>/groups/unassign', methods=['POST'])
@roles_allowed('user management')
def unassign_to_groups(user_id):
    data = loads(request.data)
    validator(assign_to_groups_validator, data)
    return service.unassign_to_groups(user_id ,data)

