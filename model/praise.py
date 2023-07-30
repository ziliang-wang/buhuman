from sqlalchemy import Table, or_
from common.database import db_connect
from app.config.config import config
from app.settings import env
from model.user import User

engine, db_session, Base = db_connect()


class Praise(Base):
    __table__ = Table('praise', Base.metadata, autoload_with=engine)

    def update_status(self, uid, aid, praised=0):
        # collected 0 收藏 1取消收藏
        row = db_session.query(Praise).filter_by(
            uid=uid,
            aid=aid,
            is_valid=1
        ).first()

        if not row:
            praise = Praise(
                uid=uid,
                aid=aid,
                praised=praised
            )
            db_session.add(praise)
        else:
            row.praised = praised
        db_session.commit()

    def get_praise_status(self, uid, aid):
        praised = db_session.query(Praise.praised).filter_by(uid=uid, aid=aid).first()
        if not praised:
            return 0
        return praised


