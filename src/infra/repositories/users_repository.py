from src.infra.repositories.base_repository import BaseRepository
from src.config import get_session
from src.domain.models.users import Users

class UsersRepository(BaseRepository):
    def __init__(self, entity):
        super().__init__(entity)

    def add_groups(self, user: Users,groups: list):
        session = get_session()
        for group in groups:
            user.groups.append(group)
        session.commit()

    def remove_groups(self, user: Users,groups: list):
        session = get_session()
        new_groups = []
        for group in user.groups:
            if group not in groups:
                new_groups.append(group)
        user.groups = new_groups
        session.commit()

    def update_password(self, user: Users,password):
        session = get_session()
        user.password = password
        session.commit()
        return user

    def read_by_email(self, email):
        session = get_session()
        return session.query(self.entity).filter_by(email=email).all()

    def read_by_email_and_password(self, email, password):
        session = get_session()
        return session.query(self.entity).filter_by(email=email, password=password).first()