from flask import Blueprint
from flask import request, Response
from json import loads
from http import HTTPStatus
from flask import jsonify

from src.services.profiles_service import ProfilesService
from src.security.security import roles_allowed
from src.utils.validator import validator
from src.utils.handlers import get_items_to_querys_from_request
from .validator import insert_profile_validator
from .validator import update_profile_validator
from .validator import filter_profile_validator

service = ProfilesService()

app = Blueprint('profiles', __name__)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('', methods=['POST'])
@roles_allowed('CREATE_PROFILES')
def create_profile():
    data = loads(request.data)
    validator(insert_profile_validator, data)
    return jsonify(service.create_profile(data)), HTTPStatus.CREATED


@app.route('', methods=['GET'])
@roles_allowed('READ_PROFILES')
def list_profiles():
    filters = get_items_to_querys_from_request()
    validator(filter_profile_validator, filters)
    return jsonify(service.list(filters))


@app.route('/<profile_id>/roles', methods=['GET'])
@roles_allowed('READ_PROFILES')
def list_roles_from_profiles(profile_id: int):
    return jsonify(service.list_roles_from_profiles(profile_id))


@app.route('/<profile_id>', methods=['PUT'])
@roles_allowed('UPDATE_PROFILES')
def update_profiles(profile_id: int):
    data = loads(request.data)
    validator(update_profile_validator, data)
    service.update_profile(profile_id, data)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/<profile_id>', methods=['DELETE'])
@roles_allowed('DELETE_PROFILES')
def delete_profile(profile_id):
    service.delete(profile_id)
    return Response(status=HTTPStatus.NO_CONTENT)
