from flask import Flask, render_template
from flask_cors import CORS

from src.routes.routes import create_routes

from src.config import Base, get_engine

def create_app(testing = False):
    app = Flask(__name__)
    CORS(app)
    
    create_routes(app)

    app.config['testing'] = testing

    if testing:
        Base.metadata.create_all(bind=get_engine(testing))

    return app

app = create_app()

@app.route('/docs')
def docs(): # pragma: no cover
    import os
    from flask import Response
    path = os.path.abspath('redoc-static.html')
    arq = open(path,'r')
    return Response(response=arq)