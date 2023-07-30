from sqlalchemy import Table, or_
from common.database import db_connect
from app.config.config import config
from app.settings import env
from model.user import User

engine, db_session, Base = db_connect()


class Collection(Base):
    __table__ = Table('collection', Base.metadata, autoload_with=engine)

    def update_status(self, uid, aid, collected=0):
        # collected 0 收藏 1取消收藏
        row = db_session.query(Collection).filter_by(
            uid=uid,
            aid=aid,
            is_valid=1
        ).first()

        if not row:
            collection = Collection(
                uid=uid,
                aid=aid,
                collected=collected
            )
            db_session.add(collection)
        else:
            row.collected = collected
        db_session.commit()

    def get_collection_status(self, uid, aid):
        collected = db_session.query(Collection.collected).filter_by(uid=uid, aid=aid).first()
        if not collected:
            return 0
        return collected[0]


