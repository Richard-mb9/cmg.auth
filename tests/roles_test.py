from http import HTTPStatus
from json import dumps, loads

from src.infra.repositories.profiles_repository import ProfilesRepository

from .fixtures.app import Client


def test_get_ping_roles_api(client: Client):
    response = client.get('/roles/ping')
    assert response.status_code == HTTPStatus.OK


def test_create_role(client: Client):
    data = dumps({'name': 'teste'})
    response = client.post('/roles', data=data)
    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in loads(response.data)


def test_fail_create_two_equal_rules(client: Client):
    data = dumps({'name': 'teste'})
    client.post('/roles', data=data)
    response = client.post('/roles', data=data)
    assert response.status_code == HTTPStatus.CONFLICT


def test_list_roles(client: Client, roles):
    response = client.get('/roles')
    data = loads(response.data)
    assert len(data) > 0


def test_update_role(client: Client, roles):
    data = dumps({'name': 'ROLE'})
    response = client.post('/roles', data=data)
    role_id = response.json['id']
    new_name = 'NEW_NAME'
    data_to_update = dumps({'name': new_name})
    response = client.put(f"/roles/{role_id}", data=data_to_update)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get('/roles')

    found_role = False
    for role in response.json:
        if role['id'] == role_id:
            assert role['name'] == new_name
            found_role = True

    assert found_role == True


def test_fail_update_two_equal_rules(client: Client):
    data = dumps({'name': 'INVALID_NAME'})
    client.post('/roles', data=data)
    data = dumps({'name': 'ROLE'})
    response = client.post('/roles', data=data)
    role_id = response.json['id']
    data_to_update = dumps({'name': 'INVALID_NAME'})
    response = client.put(f"/roles/{role_id}", data=data_to_update)
    assert response.status_code == HTTPStatus.CONFLICT


def test_fail_update_with_invalid_parameters(client: Client):
    data = dumps({'invalid': 'ROLE'})
    response = client.post('/roles', data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_delete_invalid_roles(client: Client, roles):
    response = client.delete(f'roles/{0}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_roles(client: Client, roles):
    response = client.get('/roles')
    data = loads(response.data)
    role_id = data[0]['id']

    response = client.delete(f'roles/{role_id}')
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get('/roles')
    data = loads(response.data)

    roles_ids = []
    for item in data:
        roles_ids.append(item['id'])

    assert role_id not in roles_ids
