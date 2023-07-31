from sqlalchemy import Table, or_
from common.database import db_connect
from app.config.config import config
from app.settings import env
from model.article import Article
from model.user import User

engine, db_session, Base = db_connect()


class Collection(Base):
    __table__ = Table('collection', Base.metadata, autoload_with=engine)

    def get_collection_row(self, uid, aid):
        row = db_session.query(Collection).filter_by(uid=uid, aid=aid).first()
        return row

    def update_status(self, uid, aid, collected=0):
        # article_row = db_session.query(Article).filter_by(aid=aid).first()
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
        # if row.collected == 0:
        #     if article_row.collected < 0:
        #         article_row.collected = 0
        #     article_row.collected -= 1
        # else:
        # article_row.collected = 1
        db_session.commit()

    def get_collection_status(self, uid, aid):
        collected = db_session.query(Collection.collected).filter_by(uid=uid, aid=aid).first()
        if not collected:
            return 0
        return collected[0]


