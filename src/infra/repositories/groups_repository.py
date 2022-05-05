from src.infra.repositories.base_repository import BaseRepository
from src.config import get_session
from src.domain.models.groups import Groups

class GroupsRepository(BaseRepository):
    def __init__(self, entity):
        super().__init__(entity)

    def read_by_name(self, name):
        session = get_session()
        return session.query(self.entity).filter_by(name=name).first()

    def add_roles(self, group: Groups, roles: list):
        session = get_session()
        for role in roles:
            group.roles.append(role)
        session.commit()
    
    def remove_roles(self, group: Groups, roles: list):
        session = get_session()
        new_roles = []
        for role in group.roles:
            if role not in roles:
                new_roles.append(role)
        group.roles = new_roles
        session.commit()