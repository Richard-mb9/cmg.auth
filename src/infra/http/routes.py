from flask import Flask

from src.infra.http.users.api import app as users_app
from src.infra.http.roles.api import app as roles_app
from src.infra.http.groups.api import app as groups_app

def create_routes(app: Flask):
    app.register_blueprint(users_app, url_prefix='/users')
    app.register_blueprint(roles_app, url_prefix='/roles')
    app.register_blueprint(groups_app, url_prefix='/groups')