import pytest
from src.app import create_app


@pytest.fixture(scope='session')
def app():
    app = create_app(True)

    yield app
    import os
    os.remove('file.db')

    
@pytest.fixture
def app_context(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()