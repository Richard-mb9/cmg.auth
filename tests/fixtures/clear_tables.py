import pytest
from src.domain.users import Users
from src.domain.roles import Roles
from src.domain.profiles import Profiles
from src.config import get_session


def delete_items(entity):
    session = get_session()
    list = session.query(entity).filter().all()
    for item in list:
        session.delete(item)

    session.commit()


@pytest.fixture(scope='function', autouse=True)
def clear_all_tables():
    yield
    delete_items(Users)
    delete_items(Profiles)
    delete_items(Roles)
