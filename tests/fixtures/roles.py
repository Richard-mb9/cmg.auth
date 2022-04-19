import pytest
from src.modules.auth.domain.models.roles import Roles

roles_admin = [
    'permissions management',
    'groups management',
    'user management',
    'delete groups',
    'delete roles',
    'create groups',
    'create roles'
]

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