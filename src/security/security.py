from functools import wraps
from flask import request

from src.utils.errors import AccessDeniedError, UnauthorizedError
from src.security.Auth import Auth

def get_roles():
    token = request.headers.get('access_token', None)
    if not token:
        return None
    
    jwt_payload = Auth().decodeToken(token)
    return jwt_payload.get('roles', [])


def has_role(roles):
    user_roles = get_roles()
    if isinstance(roles, list):
        for role in roles:
            if role in user_roles:
                return True
    return roles in user_roles


def roles_allowed(*roles):
    """Decorator to be used in the functions mapped as routes to check if
    the user has at least one of the roles reported"""
    def require_profile_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('access_token')
            if not token:
                UnauthorizedError("token is required")
            liberate = False
            for profile in roles:
                if has_role(profile):
                    liberate = True
            if not liberate:
                AccessDeniedError()
            return func(*args, **kwargs)
        return wrapper
    return require_profile_decorator


def login_required(func):
    @wraps(func)
    def decoretedFunction(*args, **kwargs):
        token = request.headers.get('access_token')
        if not token:
            UnauthorizedError("token is required")
        try:
            Auth().decodeToken(token)
        except Exception as error:
            return UnauthorizedError("token is invalid or expired")
        return func(*args, **kwargs)
    return decoretedFunction