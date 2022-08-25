import pytest
from src.domain.roles import Roles
from src.infra.repositories.roles_repository import RolesRepository
from src.utils.enums.roles import RolesEnum

roles_admin = [role.value for role in RolesEnum]


@pytest.fixture(scope='function')
def roles():
    list = roles_admin
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
        except Exception:
            continue
