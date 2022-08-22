from http import HTTPStatus
from json import dumps, loads

from .fixtures.app import Client


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


def test_fail_update_password_with_incorrect_old_password(client: Client, users):
    data_to_update = dumps({'old_password': 'invalid', 'new_password': '123456'})
    response = client.put(f'users/{1}/update-password', data=data_to_update)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_update_password_with_incorrect_user(client: Client, users):
    data_to_update = dumps({'old_password': 'invalid', 'new_password': '123456'})
    response = client.put(f'users/{0}/update-password', data=data_to_update)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_update_password_with_incorrect_parameters(client: Client, users):
    data_to_update = dumps({'invalid': '123456'})
    response = client.put(f'users/{1}/update-password', data=data_to_update)
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
    id = response.json['id']

    data_to_update = dumps({'enable': False})
    response = client.put(f'users/{id}', data=data_to_update)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get('/users')
    users = response.json
    assert True
