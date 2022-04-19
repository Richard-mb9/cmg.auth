from flask import Flask

from src.modules.auth.infra.http.users.api import app as users_app
from src.modules.auth.infra.http.roles.api import app as roles_app
from src.modules.auth.infra.http.groups.api import app as groups_app
from src.modules.auth.infra.http.auth.api import app as auth_app

def create_routes(app: Flask):
    app.register_blueprint(users_app, url_prefix='/users')
    app.register_blueprint(roles_app, url_prefix='/roles')
    app.register_blueprint(groups_app, url_prefix='/groups')
    app.register_blueprint(auth_app, url_prefix='/auth')