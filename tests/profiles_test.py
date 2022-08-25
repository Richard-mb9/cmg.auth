from http import HTTPStatus
from json import dumps, loads

from .fixtures.app import Client

from src.infra.repositories.roles_repository import RolesRepository
from src.infra.repositories.profiles_repository import ProfilesRepository


def test_get_ping_profiles_api(client: Client):
    response = client.get('/profiles/ping')
    assert response.status_code == HTTPStatus.OK


def test_create_profile(client: Client):
    data = dumps({'name': 'teste'})
    response = client.post('/profiles', data=data)
    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in loads(response.data)


def test_fail_create_two_equal_profiles(client: Client):
    data = dumps({'name': 'teste'})
    client.post('/profiles', data=data)
    response = client.post('/profiles', data=data)
    assert response.status_code == HTTPStatus.CONFLICT


def test_list_all_profiles(client: Client, profiles):
    response = client.get('/profiles')
    assert len(response.json) > 1


def test_fail_list_profiles_with_invalid_filters(client: Client):
    response = client.get('/profiles?invalid=invalid')
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_list_with_filter(client: Client, profiles):
    response = client.get('/profiles?name=ADMIN')
    assert len(response.json) == 1


def test_list_roles_from_profiles(client: Client, profiles, roles):
    roles_in_db = RolesRepository().list()
    profiles_in_db = ProfilesRepository().list()

    role_id = roles_in_db[0].id
    profile_id = profiles_in_db[0].id

    data = dumps({'roles_ids': [role_id]})
    client.put(f'/profiles/{profile_id}', data=data)

    response = client.get(f'/profiles/{profile_id}/roles')
    assert len(response.json) == 1

    assert response.json[0]['id'] == role_id


def test_fail_list_roles_from_profiles_not_existis(client: Client, profiles, roles):
    response = client.get('/profiles/0/roles')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_fail_update_profile_with_invalid_parameters(client: Client):
    data = dumps({'invalid': [1]})
    response = client.put('/profiles/1', data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_profile_name(client: Client, profiles, roles):
    data = dumps({'name': 'PROFILE'})
    response = client.post('/profiles', data=data)
    profile_id = response.json['id']
    new_name = 'NEW_NAME_PROFILE'
    data_to_update = dumps({'name': new_name})
    response = client.put(f'/profiles/{profile_id}', data=data_to_update)

    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get('/profiles')
    found_profile = False
    for profile in response.json:
        if profile['id'] == profile_id:
            assert profile['name'] == new_name
            found_profile = True

    assert found_profile is True


def test_fail_update_two_equal_profile_names(client: Client):
    data = dumps({'name': 'INVALID_NAME'})
    client.post('/profiles', data=data)
    data = dumps({'name': 'PROFILE'})
    response = client.post('/profiles', data=data)
    profile_id = response.json['id']
    data_to_update = dumps({'name': 'INVALID_NAME'})
    response = client.put(f"/profiles/{profile_id}", data=data_to_update)
    assert response.status_code == HTTPStatus.CONFLICT


def test_assign_roles_in_profile(client: Client, profiles, roles):
    roles_in_db = RolesRepository().list()
    profiles_in_db = ProfilesRepository().list()

    role_id = roles_in_db[0].id
    profile_id = profiles_in_db[0].id

    data = dumps({'roles_ids': [role_id]})
    response = client.put(f'/profiles/{profile_id}', data=data)

    assert response.status_code == HTTPStatus.NO_CONTENT

    profile = ProfilesRepository().read_by_id(profile_id)
    roles_in_profile = profile.roles
    assert len(roles_in_profile) == 1
    assert roles_in_profile[0].id == role_id


def test_unassign_role_in_profile(client: Client, profiles, roles):
    roles_in_db = RolesRepository().list()
    profiles_in_db = ProfilesRepository().list()

    role_id1 = roles_in_db[0].id
    role_id2 = roles_in_db[1].id
    profile_id = profiles_in_db[0].id

    data = dumps({'roles_ids': [role_id1, role_id2]})
    client.put(f'/profiles/{profile_id}', data=data)

    # passara a ter apenas a role2, removendo a role1
    data = dumps({'roles_ids': [role_id2]})
    response = client.put(f'/profiles/{profile_id}', data=data)
    assert response.status_code == HTTPStatus.NO_CONTENT

    profile = ProfilesRepository().read_by_id(profile_id)
    roles_in_profile = profile.roles
    assert len(roles_in_profile) == 1
    assert roles_in_profile[0].id == role_id2


def test_fail_delete_invalid_profile(client: Client, profiles):
    response = client.delete(f'profiles/{0}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_profiles(client: Client, profiles):
    response = client.get('/profiles')
    data = loads(response.data)
    profile_id = data[0]['id']

    response = client.delete(f'/profiles/{profile_id}')
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get('/profiles')
    data = loads(response.data)

    profiles_ids = []
    for item in data:
        profiles_ids.append(item['id'])

    assert profile_id not in profiles_ids
