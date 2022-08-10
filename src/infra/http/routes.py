from flask import Flask

from src.infra.http.users.api import app as users_app
from src.infra.http.roles.api import app as roles_app
from src.infra.http.profiles.api import app as profiles_app
from src.infra.http.auth.api import app as auth_app

def create_routes(app: Flask):
    app.register_blueprint(users_app, url_prefix='/users')
    app.register_blueprint(roles_app, url_prefix='/roles')
    app.register_blueprint(profiles_app, url_prefix='/profiles')
    app.register_blueprint(auth_app, url_prefix='/auth')