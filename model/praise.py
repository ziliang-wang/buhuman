from sqlalchemy import Table, or_
from sqlalchemy.sql.functions import sum

from common.database import db_connect
from app.config.config import config
from app.settings import env
from model.article import Article
from model.user import User

engine, db_session, Base = db_connect()


class Praise(Base):
    __table__ = Table('praise', Base.metadata, autoload_with=engine)

    def calc_praised_num(self, aid):
        praised_num = db_session.query(sum(Praise.praised)).filter_by(aid=aid, praised=1, is_valid=1).first()
        # print(praised_num, type(praised_num))
        # print('點讚數:', praised_num[0])
        return praised_num[0]

    def update_status(self, uid, aid, praised=0):
        # article_row = db_session.query(Article).filter_by(aid=aid).first()
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
        # article_row.praised = praised
        db_session.commit()
        # 計算獲讚數
        praised_num = self.calc_praised_num(aid)
        # print('點讚數:', int(praised_num))
        return praised_num

    def get_praise_status(self, uid, aid):
        praised = db_session.query(Praise.praised).filter_by(uid=uid, aid=aid).first()
        if not praised:
            return 0
        return praised[0]


