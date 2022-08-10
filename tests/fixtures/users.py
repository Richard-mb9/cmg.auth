import pytest
from src.domain.models.users import Users
from src.domain.services.users_service import UserService
from src.infra.repositories.users_repository import UsersRepository

@pytest.fixture(scope='function')
def users():
    list = ['teste@teste.com', 'user_teste@teste.com']
    list_users = []
    repository = UsersRepository()
    for email in list:
        data =  UserService().encode_password({'email':email, 'password': '123456', 'profile_id': 1})
        user =  Users(email=data['email'], password=data['password'], profile_id=data['profile_id'])
        repository.create(user)
        list_users.append(user)

    yield

    for item in list_users:
        try:
            repository.delete(item.id)
        except:
            continue