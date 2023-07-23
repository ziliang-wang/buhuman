from sqlalchemy import Table
from common.database import db_connect

engine, db_session, Base = db_connect()


class User(Base):
    __table__ = Table('user', Base.metadata, autoload_with=engine)

    def get_one(self):
        return db_session.query(User).first()
