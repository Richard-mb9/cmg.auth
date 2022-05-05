import pytest
from src.domain.models.users import Users
from src.domain.models.groups import Groups
from src.domain.models.roles import Roles
from src.domain.services.users_service import UserService
from src.domain.services.groups_service import GroupsService
from src.domain.services.roles_service import RolesService
from src.infra.repositories.users_repository import UsersRepository

@pytest.fixture(scope='function')
def users():
    list = ['teste@teste.com', 'user_teste@teste.com']
    list_users = []
    repository = UsersRepository(Users)
    for email in list:
        data =  UserService().encode_password({'email':email, 'password': '123456'})
        user =  Users(email=data['email'], password=data['password'], profile='user')
        repository.create(user)
        list_users.append(user)

    yield

    for item in list_users:
        try:
            repository.delete(item.id)
        except:
            continue