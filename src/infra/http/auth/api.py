from flask import Blueprint, request
from json import loads
from flask import jsonify
from .validators import login_validator

from src.utils.validator import validator
from src.domain.services.auth_service import AuthService

app = Blueprint('auth', __name__)

@app.route('', methods=['POST'])
def login():
    data = loads(request.data)
    validator(login_validator, data)
    return jsonify(AuthService().login(data))