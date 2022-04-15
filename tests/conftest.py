import pytest
from app import create_app
from src.domain.models.roles import Roles
from src.domain.models.users import Users

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


@pytest.fixture
def roles():
    list = ['manager', 'waiter', 'store', 'cashier']
    list_roles = []
    for name in list:
        role =  Roles(name=name).create()
        list_roles.append(role)

    yield list

    for item in list_roles:
        item.delete()


@pytest.fixture
def users():
    list = ['teste@teste.com', 'user_teste@teste.com']
    list_users = []
    for email in list:
        user =  Users(email=email, password='123456').create()
        list_users.append(user)

    yield list

    for item in list_users:
        item.delete()

