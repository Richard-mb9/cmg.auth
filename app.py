from flask import Flask
from flask_cors import CORS

from src.infra.http.users.api import app as users_app
from src.infra.http.roles.api import app as roles_app
from config import Base, get_engine

def create_app(testing = False):
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(users_app, url_prefix='/users')
    app.register_blueprint(roles_app, url_prefix='/roles')
    app.config['testing'] = testing
    if testing:
        Base.metadata.create_all(bind=get_engine(testing))
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)