from sqlalchemy import Table, or_
from sqlalchemy.sql.functions import sum

from common.database import db_connect
from app.config.config import config
from app.settings import env
# from model.article import Article
from model.user import User

engine, db_session, Base = db_connect()


class Concern(Base):
    __table__ = Table('concern', Base.metadata, autoload_with=engine)

    def calc_concerned_num(self, tid):
        concerned_num = db_session.query(sum(Concern.concerned)).filter_by(tid=tid, concerned=1, is_valid=1).first()
        # print(praised_num, type(praised_num))
        # print('點讚數:', praised_num[0])
        return concerned_num[0]

    def update_status(self, fid, tid, concerned=0):
        # article_row = db_session.query(Article).filter_by(aid=aid).first()
        # collected 0 收藏 1取消收藏
        row = db_session.query(Concern).filter_by(
            fid=fid,
            tid=tid,
            is_valid=1
        ).first()

        if not row:
            concern = Concern(
                fid=fid,
                tid=tid,
                concerned=concerned
            )
            db_session.add(concern)
        else:
            row.concerned = concerned
        # article_row.praised = praised
        db_session.commit()
        # 計算獲讚數
        concerned_num = self.calc_concerned_num(tid)
        # print('點讚數:', int(praised_num))
        return concerned_num

    def get_concern_status(self, fid, tid):
        concerned = db_session.query(Concern.concerned).filter_by(fid=fid, tid=tid).first()
        if not concerned:
            return 0
        return concerned[0]


