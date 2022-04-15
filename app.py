from flask import Flask
from flask_cors import CORS

from src.infra.http.routes import create_routes

from config import Base, get_engine

def create_app(testing = False):
    app = Flask(__name__)
    CORS(app)
    
    create_routes(app)

    app.config['testing'] = testing

    if testing:
        Base.metadata.create_all(bind=get_engine(testing))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)