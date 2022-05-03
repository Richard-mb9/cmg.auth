from http import HTTPStatus
from json import dumps, loads

from .fixtures.app import Client

from src.domain.models.users import Users
from src.domain.models.groups import Groups


def test_get_ping_users_api(client: Client):
    response = client.get('/users/ping')
    assert response.status_code == HTTPStatus.OK


def test_create_user(client: Client):
    data = dumps({'email': 'teste@teste.com', 'password': '123456', 'profile': 'user'})
    response = client.post('/users', data=data)

    assert 'id' in loads(response.data)
    assert response.status_code == HTTPStatus.CREATED


def test_fail_create_with_invalid_parameters(client: Client):
    data = dumps({'invalid': 'teste@teste.com', 'invalid2': '123456'})
    client.post('/users', data=data)
    response = client.post('/users', data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_create_two_users_with_the_same_email(client: Client):
    data = dumps({'email': 'teste@teste.com', 'password': '123456', 'profile': 'user'})
    client.post('/users', data=data)
    response = client.post('/users', data=data)
    assert response.status_code == HTTPStatus.CONFLICT


def test_fail_update_password_with_incorrect_old_password(client: Client, users):
    data_to_update = dumps({'old_password': 'invalid', 'new_password': '123456'})
    response = client.put(f'users/{1}/update-password',data=data_to_update)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_update_password_with_incorrect_user(client: Client, users):
    data_to_update = dumps({'old_password': 'invalid', 'new_password': '123456'})
    response = client.put(f'users/{0}/update-password',data=data_to_update)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_update_password_with_incorrect_parameters(client: Client, users):
    data_to_update = dumps({'invalid': '123456'})
    response = client.put(f'users/{1}/update-password',data=data_to_update)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_password(client: Client):
    data = dumps({'email': 'teste2@teste.com', 'password': '123456', 'profile': 'user'})
    response =  client.post('/users', data=data)
    id = loads(response.data)['id']

    data_to_update = dumps({'old_password': '123456', 'new_password': '123456789'})
    response = client.put(f'users/{id}/update-password',data=data_to_update)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_fail_assign_group_with_invalid_parameters(client: Client):
    data = dumps({'invalid': [1]})
    response = client.post(f'/users/1/groups/assign', data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_fail_assign_group_in_user_without_roles(client: Client):
    data = dumps({'groups_ids': [1,2]})
    response = client.roles('invalid').post(f'/users/1/groups/assign', data=data)

    assert response.status_code == HTTPStatus.FORBIDDEN

def test_fail_assign_group_in_user_without_token(client: Client):
    data = dumps({'groups_ids': [1,2]})
    response = client.post(f'/users/1/groups/assign', data=data, use_token=False)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_assign_group_in_user(client: Client, users, groups):
    users_in_db = Users().list()
    groups_in_db = Groups().list()

    user_id = users_in_db[0].id
    group_id = groups_in_db[0].id

    data = dumps({'groups_ids': [group_id]})
    response = client.post(f'/users/{user_id}/groups/assign', data=data)

    assert response.status_code == HTTPStatus.NO_CONTENT

    user = Users().read_by_id(user_id)
    groups_in_user = user.groups
    assert len(groups_in_user) == 1
    assert groups_in_user[0].id == group_id


def test_fail_unassign_group_with_invalid_parameters(client: Client):
    data = dumps({'invalid': [1]})
    response = client.post(f'/users/1/groups/unassign', data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_unassign_group_in_user(client: Client, users, groups):
    users_in_db = Users().list()
    groups_in_db = Groups().list()

    user_id = users_in_db[0].id
    group_id1 = groups_in_db[0].id
    group_id2 = groups_in_db[1].id
    data = dumps({'groups_ids': [group_id1, group_id2]})
    client.post(f'/users/{user_id}/groups/assign', data=data)

    data = dumps({'groups_ids': [group_id1]})
    response = client.post(f'/users/{user_id}/groups/unassign', data=data)
    assert response.status_code == HTTPStatus.NO_CONTENT

    user = Users().read_by_id(user_id)
    groups_in_user = user.groups
    assert len(groups_in_user) == 1
    assert groups_in_user[0].id == group_id2
