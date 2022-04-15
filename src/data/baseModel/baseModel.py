from src.config import get_session
from sqlalchemy import Column, Integer

class BaseModel:
    id = Column(Integer, primary_key=True)

    def create(self):
        session = get_session()
        session.add(self)
        session.commit()
        return self

    def delete(self):
        session = get_session()
        session.delete(self)
        session.commit()

    @classmethod
    def list(self):
        session = get_session()
        return session.query(self).filter().all()

    @classmethod
    def read_by_id(self, id):
        session = get_session()
        return session.query(self).filter_by(id=id).first()

    @classmethod
    def read_by_id_in(self, ids: list):
        session = get_session()
        return session.query(self).where(self.id.in_(ids)).all()
        
        












