from typing import List
from src.infra.repositories.base_repository import BaseRepository
from src.config import get_session
from src.domain.models.users import Users
from src.domain.models.profiles import Profiles

class UsersRepository(BaseRepository):
    def __init__(self):
        super().__init__(Users)

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
    
    def update_profiles(self, user_id, profiles_names: List[str]):
        session = get_session()
        user: Users = session.query(Users).filter_by(id=user_id).first()
        profiles: Profiles = session.query(Profiles).where(Profiles.name.in_(profiles_names)).all()
        user.profiles = profiles
        session.commit()
        