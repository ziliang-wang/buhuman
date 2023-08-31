from sqlalchemy import Table, or_
from sqlalchemy.ext.hybrid import hybrid_property

from common.database import db_connect
from app.config.config import config
from app.settings import env
# from model.article import Article
from model.user import User

engine, db_session, Base = db_connect()


class Notification(Base):
    __table__ = Table('notification', Base.metadata, autoload_with=engine)

    def update_praised_notification(self, uid, tid, aid, praised):
        notification_row = db_session.query(Notification).filter_by(
            uid=uid,
            aid=aid,
            is_valid=1
        ).first()

        if not notification_row:
            notification = Notification(
                uid=uid,
                tid=tid,
                aid=aid,
                praised=praised
            )
            db_session.add(notification)
        else:
            notification_row.praised = praised

        db_session.commit()

    def get_notification_list(self, uid):
        # db_session.query(Notification)
        pass
