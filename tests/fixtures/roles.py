import pytest
from src.domain.models.roles import Roles


@pytest.fixture(scope='function')
def roles():
    list = ['role1', 'role2', 'role3', 'role4']
    list_roles = []
    for name in list:
        role =  Roles(name=name).create()
        list_roles.append(role)

    yield list

    for item in list_roles:
        try:
            item.delete()
        except:
            continue