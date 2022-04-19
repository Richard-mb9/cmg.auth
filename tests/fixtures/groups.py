from flask import session
import pytest
from src.modules.auth.domain.models.groups import Groups

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