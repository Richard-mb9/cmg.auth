from flask import Flask, render_template
from flask_cors import CORS

from src.infra.http.routes import create_routes

from src.config import Base, get_engine


def create_app():
    app = Flask(__name__)
    CORS(app)

    create_routes(app)
    return app


app = create_app()


@app.route('/docs')
def docs():  # pragma: no cover
    import os
    from flask import Response
    path = os.path.abspath('redoc-static.html')
    arq = open(path, 'r')
    return Response(response=arq)
