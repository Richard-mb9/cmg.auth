from http import HTTPStatus
from flask import Blueprint
from flask import request, Response
from json import loads

from src.domain.services.users_service import UserService

service = UserService()

app = Blueprint('users',__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
def insert_user():
    user_data = loads(request.data)
    return Response(service.create_user(user_data), status=HTTPStatus.CREATED)


@app.route('/<user_id>/update-password', methods=['PUT'])
def update_password(user_id):
    data = loads(request.data)
    return service.update_password(user_id ,data)


@app.route('/<user_id>/roles/assign', methods=['POST'])
def assign_to_roles(user_id):
    data = loads(request.data)
    return service.assign_to_roles(user_id ,data)


@app.route('/<user_id>/roles/unassign', methods=['POST'])
def unassign_to_roles(user_id):
    data = loads(request.data)
    return service.unassign_to_roles(user_id ,data)

