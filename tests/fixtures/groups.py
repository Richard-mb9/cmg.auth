import pytest
from src.domain.models.groups import Groups

@pytest.fixture(scope='function')
def groups():
    list = ['manager', 'waiter', 'store', 'cashier']
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