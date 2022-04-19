import pytest
from src.modules.auth.domain.models.users import Users
from src.modules.auth.domain.models.groups import Groups
from src.modules.auth.domain.models.roles import Roles
from src.modules.auth.domain.services.users_service import UserService
from src.modules.auth.domain.services.groups_service import GroupsService
from src.modules.auth.domain.services.roles_service import RolesService

@pytest.fixture(scope='function')
def users():
    list = ['teste@teste.com', 'user_teste@teste.com']
    list_users = []
    for email in list:
        data =  UserService().encode_password({'email':email, 'password': '123456'})
        user =  Users(email=data['email'], password=data['password']).create()
        list_users.append(user)

    yield

    for item in list_users:
        try:
            item.delete()
        except:
            continue