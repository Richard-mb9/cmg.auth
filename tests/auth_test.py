from http import HTTPStatus
from json import dumps, loads

from .fixtures.app import Client

def test_get_token_fail_for_incorrect_credentials(client: Client, users):
    data = dumps({'email': 'teste@teste.com', 'password': 'invalid'})
    response = client.post('/auth', data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_token(client: Client, users):
    data = dumps({'email': 'teste@teste.com', 'password': '123456'})
    response = client.post('/auth', data=data)

    assert response.status_code == HTTPStatus.OK
    assert 'token' in loads(response.data)



