from http import HTTPStatus
from json import dumps, loads

from .fixtures.app import Client

from src.domain.models.roles import Roles
from src.domain.models.profiles import Profiles
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


def test_list_profiles(client: Client, profiles):
    response = client.get('/profiles')
    data = loads(response.data)
    assert len(data) > 0


def test_fail_assign_role_with_invalid_parameters(client: Client):
    data = dumps({'invalid': [1]})
    response = client.post(f'/profiles/1/roles/assign', data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST 


def test_assign_roles_in_profile(client: Client, profiles, roles):
    roles_in_db = RolesRepository().list()
    profiles_in_db = ProfilesRepository().list()

    role_id = roles_in_db[0].id
    profile_id = profiles_in_db[0].id

    data = dumps({'roles_ids': [role_id]})
    response = client.post(f'/profiles/{profile_id}/roles/assign', data=data)

    assert response.status_code == HTTPStatus.NO_CONTENT

    profile = ProfilesRepository().read_by_id(profile_id)
    roles_in_profile = profile.roles
    assert len(roles_in_profile) == 1
    assert roles_in_profile[0].id == profile_id


def test_fail_unassign_role_with_invalid_parameters(client: Client):
    data = dumps({'invalid': [1]})
    response = client.post(f'/profiles/1/roles/unassign', data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_unassign_role_in_profile(client: Client, profiles, roles):
    roles_in_db = RolesRepository().list()
    profiles_in_db = ProfilesRepository().list()

    role_id1 = roles_in_db[0].id
    role_id2 = roles_in_db[1].id
    profile_id = profiles_in_db[0].id

    data = dumps({'roles_ids': [role_id1, role_id2]})
    client.post(f'/profiles/{profile_id}/roles/assign', data=data)

    data = dumps({'roles_ids': [role_id1]})
    response = client.post(f'/profiles/{profile_id}/roles/unassign', data=data)
    assert response.status_code == HTTPStatus.NO_CONTENT

    profile = ProfilesRepository().read_by_id(profile_id)
    roles_in_profile = profile.roles
    assert len(roles_in_profile) == 1
    assert roles_in_profile[0].id == role_id2


def test_fail_delete_invalid_profile(client: Client, profiles):
    response =  client.delete(f'profiles/{0}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_profiles(client: Client, profiles):
    response = client.get('/profiles')
    data = loads(response.data)
    profile_id = data[0]['id']

    response =  client.delete(f'/profiles/{profile_id}')
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = client.get('/profiles')
    data = loads(response.data)

    profiles_ids = []
    for item in data:
        profiles_ids.append(item['id'])

    
    assert profile_id not in profiles_ids