import pytest
from src.domain.models.roles import Roles
from src.infra.repositories.roles_repository import RolesRepository

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
    repository = RolesRepository(Roles)
    for name in list:
        role = Roles(name=name)
        role =  repository.create(role)
        list_roles.append(role)

    yield list

    for item in list_roles:
        try:
            repository.delete(item.id)
        except:
            continue