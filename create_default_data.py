from src.config import get_session
from src.utils.enums.profiles import ProfilesEnum
from src.utils.enums.roles import RolesEnum
from src.domain.models.users import Users
from src.domain.models.profiles import Profiles
from src.domain.models.roles import Roles
from src.domain.services.roles_service import RolesService
from src.domain.services.profiles_service import ProfilesService
from src.infra.repositories.profiles_repository import ProfilesRepository
from src.infra.repositories.roles_repository import RolesRepository
from src.infra.repositories.users_repository import UsersRepository



""" list_profiles = [profile.value for profile in ProfilesEnum]

repository = ProfilesRepository()
for name in list_profiles:
    profile =  Profiles(name=name)
    profile = repository.create(profile) """


""" list_roles = [role.value for role in RolesEnum]
lista = []
for role in list_roles:
    role = Roles(name=role)
    lista.append(role) """


session = get_session()
""" for role in lista:
    session.add(role) """

roles = session.query(Roles).filter().all()
profile: Profiles = session.query(Profiles).filter_by(name="ADMIN").first()
profile.roles = roles

session.commit()

""" user = Users(email='admin@admin.com', password='123456', profile_id=1)
UsersRepository().create(user) """