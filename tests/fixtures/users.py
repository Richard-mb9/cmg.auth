import pytest
from src.domain.profiles import Profiles
from src.config import get_session
from src.domain.users import Users
from src.services.users_service import UserService
from src.infra.repositories.users_repository import UsersRepository


@pytest.fixture(scope='function')
def users(profiles):
    list = ['teste@teste.com', 'user_teste@teste.com']
    list_users = []
    repository = UsersRepository()
    session = get_session()
    """ for email in list:
        data =  UserService().encode_password({'email':email, 'password': '123456'})
        user =  Users(email=data['email'], password=data['password'])
        repository.create(user)
        list_users.append(user) """
    for email in list:
        password = UserService().encode_password('123456')
        user_data = {'email': email, 'password': password, 'profiles': ['USER']}
        list_profiles = session.query(Profiles).where(Profiles.name.in_(user_data['profiles'])).all()
        user = Users(
            email=user_data['email'],
            password=user_data['password'],
            profiles=list_profiles
        )
        session.add(user)
        list_users.append(user)

    session.commit()

    yield

    for item in list_users:
        try:
            repository.delete(item.id)
        except Exception:
            continue
