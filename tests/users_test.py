from http import HTTPStatus
from json import dumps, loads

from .fixtures.app import Client
from src.infra.repositories.users_repository import UsersRepository
from src.infra.repositories.profiles_repository import ProfilesRepository


def test_get_ping_users_api(client: Client):
    response = client.get('/users/ping')
    assert response.status_code == HTTPStatus.OK


def test_create_user(client: Client, profiles):
    data = dumps({'email': 'teste_create_user@teste.com', 'password': '123456', 'profiles': ['USER']})
    response = client.post('/users', data=data)

    assert 'id' in loads(response.data)
    assert response.status_code == HTTPStatus.CREATED


def test_fail_create_with_invalid_parameters(client: Client):
    data = dumps({'invalid': 'teste@teste.com', 'invalid2': '123456'})
    client.post('/users', data=data)
    response = client.post('/users', data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_create_two_users_with_the_same_email(client: Client, profiles):
    data = dumps({'email': 'teste@teste.com', 'password': '123456', 'profiles': ['USER']})
    client.post('/users', data=data)
    response = client.post('/users', data=data)
    assert response.status_code == HTTPStatus.CONFLICT


def test_fail_create_user_without_role_for_create_profile(client: Client, profiles):
    data = dumps({'name': 'PROFILE', 'role_name': 'CREATE_USER_WITH_PROFILE'})
    client.post('/profiles', data=data)
    data = dumps({'email': 'teste@teste.com', 'password': '123456', 'profiles': ['PROFILE']})
    response = client.roles('WITHOUT_ROLE').post('/users', data=data)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_fail_create_user_with_invalid_profile(client: Client, profiles):
    data = dumps({'email': 'teste@teste.com', 'password': '123456', 'profiles': ['INVALID']})
    client.roles('WITHOUT_ROLE').post('/users', data=data)
    response = client.post('/users', data=data)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_fail_update_password_with_incorrect_old_password(client: Client, users):
    data = dumps({'email': 'teste2@teste.com', 'password': '12345678', 'profiles': ['USER']})
    response = client.post('/users', data=data)
    user_id = response.json['id']

    data_to_update = dumps({'old_password': 'invalid', 'new_password': '123456'})
    response = client.put(f'users/{user_id}/update-password', data=data_to_update)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_update_password_with_incorrect_user(client: Client, users):
    data_to_update = dumps({'old_password': 'invalid', 'new_password': '123456'})
    response = client.put(f'users/{0}/update-password', data=data_to_update)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_update_password_with_incorrect_parameters(client: Client, users):
    data = dumps({'email': 'teste2@teste.com', 'password': '123456', 'profiles': ['USER']})
    response = client.post('/users', data=data)
    user_id = response.json['id']

    data_to_update = dumps({'invalid': '123456'})
    response = client.put(f'users/{user_id}/update-password', data=data_to_update)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_password(client: Client, profiles):
    data = dumps({'email': 'teste2@teste.com', 'password': '123456', 'profiles': ['USER']})
    response = client.post('/users', data=data)
    id = loads(response.data)['id']

    data_to_update = dumps({'old_password': '123456', 'new_password': '123456789'})
    response = client.put(f'users/{id}/update-password', data=data_to_update)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_update_user(client: Client, profiles):
    data = dumps({'email': 'teste2@teste.com', 'password': '123456', 'profiles': ['USER']})
    response = client.post('/users', data=data)
    user_id = response.json['id']

    data_to_update = dumps({'enable': False})
    response = client.put(f'users/{user_id}', data=data_to_update)
    assert response.status_code == HTTPStatus.NO_CONTENT

    user = UsersRepository().read_by_id(user_id)
    assert user.enable is False


def test_update_user_profiles(client: Client, users, profiles):
    users_in_db = UsersRepository().list()
    profiles_in_db = ProfilesRepository().list()

    user = users_in_db[0]
    profile1 = profiles_in_db[0]
    profile2 = profiles_in_db[1]

    data = dumps({'profiles': [profile1.name, profile2.name]})
    response = client.put(f'users/{user.id}/profiles', data=data)

    user = UsersRepository().read_by_id(user.id)

    found_profile_1 = False
    found_profile_2 = False

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(user.profiles) == 2

    for profile in user.profiles:
        if profile.id == profile1.id:
            found_profile_1 = True
        elif profile.id == profile2.id:
            found_profile_2 = True

    assert found_profile_1 is True
    assert found_profile_2 is True


def test_filter_user_by_id(client: Client, profiles):
    data = dumps({'email': 'teste2@teste.com', 'password': '123456', 'profiles': ['USER']})
    response = client.post('/users', data=data)
    user_id = response.json['id']

    response = client.get(f'/users?id={user_id}')

    assert len(response.json) == 1
    assert response.json[0]['id'] == user_id


def test_filter_user_by_email(client: Client, profiles):
    email = 'teste2@teste.com'
    data = dumps({'email': email, 'password': '123456', 'profiles': ['USER']})
    response = client.post('/users', data=data)

    response = client.get(f'/users?email={email}')

    assert len(response.json) == 1
    assert response.json[0]['email'] == email


def test_filter_user_by_profile(client: Client, profiles):
    data = dumps({'email': 'teste@teste.com', 'password': '123456', 'profiles': ['USER']})
    response = client.post('/users', data=data)
    user_id_1 = response.json['id']
    data = dumps({'email': 'teste1@teste.com', 'password': '123456', 'profiles': ['USER']})
    response = client.post('/users', data=data)
    user_id_2 = response.json['id']
    data = dumps({'email': 'teste2@teste.com', 'password': '123456', 'profiles': ['ADMIN']})
    response = client.profile(['ADMIN']).post('/users', data=data)
    user_id_3 = response.json['id']

    response = client.get('/users?profile=ADMIN')

    assert len(response.json) == 1
    assert response.json[0]['id'] == user_id_3

    response = client.get('/users?profile=USER')

    ids = []
    for user in response.json:
        ids.append(user['id'])
    assert len(ids) == 2
    assert user_id_1 in ids and user_id_2 in ids
