from http import HTTPStatus
from flask import Blueprint, Response
from flask import request
from flask import jsonify
from json import loads


from src.security.security import login_required, roles_allowed
from src.domain.services.users_service import UserService
from src.utils.validator import validator
from src.utils.handlers import get_items_to_querys_from_request
from .validators import insert_user_validator
from .validators import update_password_validator
from .validators import update_user_profiles_validator
from .validators import update_user_validator
from .validators import filter_users_validator


service = UserService()

app = Blueprint('users', __name__)


@app.route('/ping', methods=['GET'])
def ping():
    from src.config import is_testing
    print(is_testing())
    return 'pong'


@app.route('', methods=['POST'])
def insert_user():
    user_data = loads(request.data)
    validator(insert_user_validator, user_data)
    return jsonify(service.create_user(user_data)), HTTPStatus.CREATED


@app.route('', methods=['GET'])
@roles_allowed('READ_USERS')
def list_users():
    filters = get_items_to_querys_from_request()
    validator(filter_users_validator, filters)
    return jsonify(service.list_users(filters))


@app.route('/<user_id>', methods=['PUT'])
@roles_allowed('UPDATE_USERS')
def update_user(user_id):
    data = loads(request.data)
    validator(update_user_validator, data)
    service.update(user_id, data)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/<user_id>/profiles', methods=['PUT'])
@roles_allowed('UPDATE_USERS')
def update_user_profiles(user_id):
    data = loads(request.data)
    validator(update_user_profiles_validator, data)
    service.update_user_profiles(user_id, data)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/<user_id>/update-password', methods=['PUT'])
@login_required
def update_password(user_id):
    data = loads(request.data)
    validator(update_password_validator, data)
    return service.update_password(user_id, data)
