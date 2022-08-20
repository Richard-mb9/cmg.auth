from sqlalchemy.engine import Result
from src.config import get_session


class BaseRepository:
    def __init__(self, entity):
        self.entity = entity

    def create(self, entity):
        session = get_session()
        session.add(entity)
        session.commit()
        return entity

    def delete(self, id):
        session = get_session()
        entity = self.read_by_id(id)
        session.delete(entity)
        session.commit()

    def update(self, id, data_to_update):
        session = get_session()
        entity = self.read_by_id(id)
        for key in data_to_update:
            setattr(entity, key, data_to_update[key])
        session.commit()
        return entity

    def batch_delete(self, ids):
        session = get_session()
        for id in ids:
            entity = self.read_by_id(id)
            session.delete(entity)
        session.commit()


    def list(self):
        session = get_session()
        return session.query(self.entity).filter().all()
    
    def read_by_id(self, id):
        session = get_session()
        return session.query(self.entity).filter_by(id=id).first()
    
    def read_by_id_in(self, ids: list):
        session = get_session()
        return session.query(self.entity).where(self.entity.id.in_(ids)).all()
    
    def format_search_query(self, result):
        columns = [desc[0] for desc in result.cursor.description]
        datas = []
        for item in result:
            i = 0
            data = {}
            for col in columns:
                data[col] = item[i]
                i += 1
            datas.append(data)
        return datas
