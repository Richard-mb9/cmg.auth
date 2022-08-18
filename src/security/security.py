from functools import wraps
from flask import request

from src.utils.errors import AccessDeniedError, UnauthorizedError
from src.security.Auth import Auth


def get_token():
    token = request.headers.get('authorization', None)
    if token is not None and 'Bearer' in token:
        token = token.split(' ')[1]
        return token
    else:
        return


def is_authenticated():
    token = get_token()
    return token is not None


def get_roles():
    token = get_token()
    if not token:
        return
    
    jwt_payload = Auth().decodeToken(token)
    return jwt_payload.get('roles', [])


def get_profile():
    token = get_token()
    if not token:
        return
    
    jwt_payload = Auth().decodeToken(token)
    return jwt_payload.get('profile')


def has_role(roles):
    user_roles = get_roles()
    return roles in user_roles


def has_profile(*profiles):
    user_profiles = get_profile()
    for profile in user_profiles:
        if profile in profiles:
            return True
    return False


def roles_allowed(*roles):
    """Decorator to be used in the functions mapped as routes to check if
    the user has at least one of the roles reported"""
    def require_profile_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = get_token()
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
        token = get_token()
        if not token:
            UnauthorizedError("token is required")
        try:
            Auth().decodeToken(token)
        except Exception as error:
            return UnauthorizedError("token is invalid or expired")
        return func(*args, **kwargs)
    return decoretedFunction