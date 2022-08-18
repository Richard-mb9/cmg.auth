from typing import List

from src.infra.repositories.base_repository import BaseRepository
from src.config import get_session
from src.domain.models.profiles import Profiles
from src.domain.models.roles import Roles

class ProfilesRepository(BaseRepository):
    def __init__(self):
        super().__init__(Profiles)

    def read_by_name(self, name):
        session = get_session()
        return session.query(self.entity).filter_by(name=name).first()
    
    def update_roles(self, profile: Profiles, roles: List[Roles]):
        session = get_session()
        profile.roles = roles
        session.commit()

    def add_roles(self, profile: Profiles, roles: list):
        session = get_session()
        for role in roles:
            profile.roles.append(role)
        session.commit()
    
    def remove_roles(self, profile: Profiles, roles: list):
        session = get_session()
        new_roles = []
        for role in profile.roles:
            if role not in roles:
                new_roles.append(role)
        profile.roles = new_roles
        session.commit()
    
    def list_by_name_in(self, names: List[str]) -> List[Profiles]:
        session = get_session()
        return session.query(self.entity).where(self.entity.name.in_(names)).all()