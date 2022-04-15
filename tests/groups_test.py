from http import HTTPStatus
from json import dumps, loads

from flask.testing import FlaskClient

from src.domain.models.roles import Roles
from src.domain.models.groups import Groups


def test_get_ping_groups_api(client: FlaskClient):
    response = client.get('/groups/ping')
    assert response.status_code == HTTPStatus.OK


def test_create_group(client: FlaskClient):
    data = dumps({'name': 'teste'})
    response = client.post('/groups', data=data)
    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in loads(response.data)


def test_fail_create_two_equal_groups(client: FlaskClient):
    data = dumps({'name': 'teste'})
    client.post('/groups', data=data)
    response = client.post('/groups', data=data)
    assert response.status_code == HTTPStatus.CONFLICT


def test_list_groups(client: FlaskClient, groups):
    response = client.get('/groups')
    data = loads(response.data)
    assert len(data) > 0


def test_fail_assign_role_with_invalid_parameters(client: FlaskClient):
    data = dumps({'invalid': [1]})
    response = client.post(f'/groups/1/roles/assign', data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST 


def test_assign_roles_in_group(client: FlaskClient, groups, roles):
    roles_in_db = Roles().list()
    groups_in_db = Groups().list()

    role_id = roles_in_db[0].id
    group_id = groups_in_db[0].id

    data = dumps({'roles_ids': [role_id]})
    response = client.post(f'/groups/{group_id}/roles/assign', data=data)

    assert response.status_code == HTTPStatus.NO_CONTENT

    group = Groups().read_by_id(group_id)
    roles_in_group = group.roles
    assert len(roles_in_group) == 1
    assert roles_in_group[0].id == group_id


def test_fail_unassign_role_with_invalid_parameters(client: FlaskClient):
    data = dumps({'invalid': [1]})
    response = client.post(f'/groups/1/roles/unassign', data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_unassign_role_in_group(client: FlaskClient, groups, roles):
    roles_in_db = Roles().list()
    groups_in_db = Groups().list()

    role_id1 = roles_in_db[0].id
    role_id2 = roles_in_db[1].id
    group_id = groups_in_db[0].id

    data = dumps({'roles_ids': [role_id1, role_id2]})
    client.post(f'/groups/{group_id}/roles/assign', data=data)

    data = dumps({'roles_ids': [role_id1]})
    response = client.post(f'/groups/{group_id}/roles/unassign', data=data)
    assert response.status_code == HTTPStatus.NO_CONTENT

    group = Groups().read_by_id(group_id)
    roles_in_group = group.roles
    assert len(roles_in_group) == 1
    assert roles_in_group[0].id == role_id2


def test_fail_delete_invalid_group(client: FlaskClient, groups):
    response =  client.delete(f'groups/{0}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_groups(client: FlaskClient, groups):
    response = client.get('/groups')
    data = loads(response.data)
    group_id = data[0]['id']

    response =  client.delete(f'/groups/{group_id}')
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get('/groups')
    data = loads(response.data)

    groups_ids = []
    for item in data:
        groups_ids.append(item['id'])

    
    assert group_id not in groups_ids