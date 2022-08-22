import pytest
from src.domain.models.roles import Roles
from src.infra.repositories.roles_repository import RolesRepository
from src.utils.enums.roles import RolesEnum

roles_admin = [profile.value for profile in RolesEnum]


@pytest.fixture(scope='function')
def roles():
    list = ['role1', 'role2', 'role3', 'role4']
    list_roles = []
    repository = RolesRepository()
    for name in list:
        role = Roles(name=name)
        role = repository.create(role)
        list_roles.append(role)

    yield list

    for item in list_roles:
        try:
            repository.delete(item.id)
        except:
            continue
