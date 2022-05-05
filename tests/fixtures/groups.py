import pytest
from src.domain.models.groups import Groups
from src.infra.repositories.groups_repository import GroupsRepository

@pytest.fixture(scope='function')
def groups():
    list = ['manager', 'waiter', 'store', 'cashier']
    list_groups = []
    repository = GroupsRepository(Groups)
    for name in list:
        group =  Groups(name=name)
        group = repository.create(group)
        list_groups.append(group)

    yield

    for item in list_groups:
        try:
            repository.delete(item.id)
        except:
            continue


@pytest.fixture(scope='session')
def group_admin():
    list = ['admin']
    list_groups = []
    for name in list:
        group =  Groups(name=name).create()
        list_groups.append(group)

    yield

    for item in list_groups:
        try:
            item.delete()
        except:
            continue