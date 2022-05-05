from src.infra.repositories.base_repository import BaseRepository
from src.config import get_session

class RolesRepository(BaseRepository):
    def __init__(self, entity):
        super().__init__(entity)

    def read_by_name(self, name):
        session = get_session()
        return session.query(self.entity).filter_by(name=name).all()