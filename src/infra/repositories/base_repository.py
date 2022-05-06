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