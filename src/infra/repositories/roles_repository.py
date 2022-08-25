from src.infra.repositories.base_repository import BaseRepository
from src.config import get_session
from src.domain.roles import Roles
from src.infra.repositories.schemas.list_roles_response import ListRolesResponse


class RolesRepository(BaseRepository):
    def __init__(self):
        super().__init__(Roles)

    def read_by_name(self, name):
        session = get_session()
        return session.query(self.entity).filter_by(name=name).all()

    def list_roles(self, filters: dict = {}) -> ListRolesResponse:
        query = f"select * from roles where name like '%{filters.get('name', '')}%'"
        session = get_session()
        roles = session.execute(query)
        return self.format_search_query(roles)
