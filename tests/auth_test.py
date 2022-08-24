from mockito import when, unstub
from http import HTTPStatus
from json import dumps, loads
from src.services.auth_service import AuthService
from src.infra.repositories.users_repository import UsersRepository


from .fixtures.app import Client


def test_get_token_fail_for_incorrect_credentials(client: Client, users):
    data = dumps({'email': 'teste@teste.com', 'password': 'invalid'})
    response = client.post('/auth', data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_token_fail_for_user_desable(client: Client, users):
    user = UsersRepository().read_by_email('teste@teste.com')
    UsersRepository().update(user.id, {'enable': False})
    client.put(f'/users/{user.id}', data=dumps({'enable': False}))

    data = dumps({'email': 'teste@teste.com', 'password': '123456'})
    response = client.post('/auth', data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['error'] == 'incorrect credentials'


def test_get_token_fail_for_user_invalid(client: Client, users):
    data = dumps({'email': 'invalid@teste.com', 'password': '123456'})
    response = client.post('/auth', data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['error'] == 'incorrect credentials'


def test_should_block_user_after_5_attempts(client: Client, users):
    data = dumps({'email': 'teste@teste.com', 'password': 'invalid'})
    client.post('/auth', data=data)
    client.post('/auth', data=data)
    client.post('/auth', data=data)
    client.post('/auth', data=data)
    client.post('/auth', data=data)
    response = client.post('/auth', data=data)

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_should_release_user_after_10_min(client: Client, users):
    data = dumps({'email': 'teste@teste.com', 'password': 'invalid'})
    client.post('/auth', data=data)
    client.post('/auth', data=data)
    client.post('/auth', data=data)
    client.post('/auth', data=data)
    client.post('/auth', data=data)
    response = client.post('/auth', data=data)

    assert response.status_code == HTTPStatus.FORBIDDEN

    when(AuthService).get_interval_last_tryed_invalid(...).thenReturn(11)

    data = dumps({'email': 'teste@teste.com', 'password': '123456'})
    response = client.post('/auth', data=data)

    unstub()

    assert response.status_code == HTTPStatus.OK
    response_data = loads(response.data)
    assert 'access_token' in response_data
    assert 'token_type' in response_data
    assert response_data['token_type'] == 'Bearer'


def test_get_token(client: Client, users, profiles):
    data = dumps({'email': 'teste@teste.com', 'password': '123456'})
    response = client.post('/auth', data=data)

    assert response.status_code == HTTPStatus.OK
    response_data = loads(response.data)
    assert 'access_token' in response_data
    assert 'token_type' in response_data
    assert response_data['token_type'] == 'Bearer'
