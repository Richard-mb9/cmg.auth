from http import HTTPStatus
from flask import Blueprint
from flask import request
from flask import jsonify
from json import loads

from src.security.security import login_required, roles_allowed
from src.domain.services.users_service import UserService
from src.utils.validator import validator
from .validators import insert_user_validator
from .validators import update_password_validator


service = UserService()

app = Blueprint('users',__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
def insert_user():
    user_data = loads(request.data)
    validator(insert_user_validator, user_data)
    return jsonify(service.create_user(user_data)), HTTPStatus.CREATED


@app.route('/<user_id>/update-password', methods=['PUT'])
@login_required
def update_password(user_id):
    data = loads(request.data)
    validator(update_password_validator, data)
    return service.update_password(user_id, data)

