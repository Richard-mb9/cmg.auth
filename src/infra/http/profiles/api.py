from flask import Blueprint
from flask import request, Response
from json import dumps, loads
from http import HTTPStatus
from flask import jsonify

from src.domain.services.profiles_service import ProfilesService
from src.security.security import login_required, roles_allowed
from src.utils.validator import validator
from .validator import assign_to_rules_validator
from .validator import insert_profile_validator

service = ProfilesService()

app = Blueprint('profiles',__name__)


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
@roles_allowed('CREATE_PROFILES', 'READ_PROFILES')
def list_profiles():
    return jsonify(service.list())


@app.route('/<profile_id>/roles', methods=['GET'])
@roles_allowed('CREATE_PROFILES', 'READ_PROFILES')
def list_roles_from_profiles(profile_id: int):
    return jsonify(service.list_roles_from_profiles(profile_id))


@app.route('/<profile_id>', methods=['DELETE'])
@roles_allowed('DELETE_PROFILES')
def delete_profile(profile_id):
    service.delete(profile_id)
    return Response(status=HTTPStatus.NO_CONTENT)


@app.route('/<profile_id>/roles/assign', methods=['POST'])
@roles_allowed('PROFILES_MANAGEMENT')
def assign_to_roles(profile_id):
    data = loads(request.data)
    validator(assign_to_rules_validator, data)
    return service.assign_to_roles(profile_id ,data)


@app.route('/<profile_id>/roles/unassign', methods=['POST'])
@roles_allowed('PROFILES_MANAGEMENT')
def unassign_to_roles(profile_id):
    data = loads(request.data)
    validator(assign_to_rules_validator, data)
    return service.unassign_to_roles(profile_id ,data)

