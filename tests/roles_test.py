from http import HTTPStatus
from json import dumps, loads

from flask.testing import FlaskClient

def test_get_ping_roles_api(client: FlaskClient):
    response = client.get('/roles/ping')
    assert response.status_code == HTTPStatus.OK


def test_create_role(client: FlaskClient):
    data = dumps({'name': 'teste'})
    response = client.post('/roles', data=data)
    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in loads(response.data)


def test_fail_create_two_equal_rules(client: FlaskClient):
    data = dumps({'name': 'teste'})
    client.post('/roles', data=data)
    response = client.post('/roles', data=data)
    assert response.status_code == HTTPStatus.CONFLICT


def test_list_roles(client: FlaskClient, roles):
    response = client.get('/roles')
    data = loads(response.data)
    assert len(data) > 0


def test_fail_delete_invalid_roles(client: FlaskClient, roles):
    response =  client.delete(f'roles/{0}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_roles(client: FlaskClient, roles):
    response = client.get('/roles')
    data = loads(response.data)
    role_id = data[0]['id']

    response =  client.delete(f'roles/{role_id}')
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get('/roles')
    data = loads(response.data)

    roles_ids = []
    for item in data:
        roles_ids.append(item['id'])

    
    assert role_id not in roles_ids
