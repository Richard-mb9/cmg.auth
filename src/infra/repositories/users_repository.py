from typing import List
from src.infra.repositories.base_repository import BaseRepository
from src.infra.repositories.schemas.list_users_response import ListUsersResponse
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
    
    def list_users(self, filters: dict = {})-> ListUsersResponse:
        page = int(filters.get('page', 1))
        page_size = int(filters.get('page_size', 1000))
        enable = filters.get('enable')
        profile = filters.get('profiles')
        id = filters.get('id')
        if id is not None and not id:
            del filters['id']
        if enable is not None and enable =='all':
            del filters['enable']
        if profile is not None and 'all' in profile:
            del filters['profiles']

        session = get_session()
        query = \
            f'''
            select u.id, u.email, pr.profiles, u."enable"
            from users u
            left join (
                select up.user_id as id, array_agg(p.name) as profiles 
                from user_profiles up
                left join profiles p on p.id = up.profile_id
                group by up.user_id
            ) as pr using(id)
            where  (
                    {filters.get('profiles') is None} or exists(
                    select p2.name from profiles p2
                    inner join user_profiles up2 on up2.profile_id = p2.id and up2.user_id = u.id
                    where p2.name in (SELECT unnest(ARRAY{[profile for profile in filters.get('profiles',[''])]}))
                )
            ) and (
                {filters.get('id') is None} or u.id = {filters.get('id', 0)}
            )and (
                {filters.get('email') is None} or u.email like '%{filters.get('email', '')}%'
            )
            and (
                {filters.get('enable') is None} or u.enable = {filters.get('enable', True)}
            )
            limit {page_size}
            offset {(page - 1) * page_size}
            '''
        users = session.execute(query)
        return self.format_search_query(users)

        