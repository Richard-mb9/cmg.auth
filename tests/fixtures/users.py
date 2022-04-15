import pytest
from src.domain.models.users import Users

@pytest.fixture(scope='function')
def users():
    list = ['teste@teste.com', 'user_teste@teste.com']
    list_users = []
    for email in list:
        user =  Users(email=email, password='123456').create()
        list_users.append(user)

    yield

    for item in list_users:
        try:
            item.delete()
        except:
            continue