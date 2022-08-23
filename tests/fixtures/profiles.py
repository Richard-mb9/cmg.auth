import pytest
from src.domain.models.profiles import Profiles
from src.infra.repositories.profiles_repository import ProfilesRepository
from src.utils.enums.profiles import ProfilesEnum
from src.config import get_session


@pytest.fixture(scope='function')
def profiles():
    list = [profile.value for profile in ProfilesEnum]
    list_profiles = []
    repository = ProfilesRepository()
    for name in list:
        profile = Profiles(name=name)
        profile = repository.create(profile)
        list_profiles.append(profile)

    yield

    for item in list_profiles:
        try:
            repository.delete(item.id)
        except Exception:
            continue


@pytest.fixture(scope='session')
def profile_admin():
    list = ['ADMIN']
    list_profiles = []
    repository = ProfilesRepository()
    for name in list:
        profile = Profiles(name=name)
        profile = repository.create(profile)
        list_profiles.append(profile)

    yield

    for item in list_profiles:
        try:
            item.delete()
        except:
            continue
