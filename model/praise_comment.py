from sqlalchemy import Table, or_
from sqlalchemy.sql.functions import sum

from common.database import db_connect
from app.config.config import config
from app.settings import env
# from model.article import Article
from model.user import User

engine, db_session, Base = db_connect()


class PraiseComment(Base):
    __table__ = Table('praise_comment', Base.metadata, autoload_with=engine)

    def calc_praised_num(self, comment_id):
        praised_num = db_session.query(sum(PraiseComment.praised)).filter_by(
            comment_id=comment_id,
            praised=1,
            is_valid=1).first()

        if not praised_num[0]:
            return 0
        return praised_num[0]

    def update_status(self, uid, comment_id, praised=0):
        # article_row = db_session.query(Article).filter_by(aid=aid).first()
        # collected 0 收藏 1取消收藏
        row = db_session.query(PraiseComment).filter_by(
            uid=uid,
            comment_id=comment_id,
            is_valid=1
        ).first()

        if not row:
            praise = PraiseComment(
                uid=uid,
                comment_id=comment_id,
                praised=praised
            )
            db_session.add(praise)
        else:
            row.praised = praised
        # article_row.praised = praised
        db_session.commit()
        # 計算獲讚數
        praised_num = self.calc_praised_num(comment_id)
        # print('點讚數:', int(praised_num))
        return praised_num

    def get_praise_status(self, uid, comment_id):
        praised = db_session.query(PraiseComment.praised).filter_by(uid=uid, comment_id=comment_id, is_valid=1).first()
        print(praised)
        if not praised:
            return 0
        return praised[0]

    def get_all_praise_comment(self):
        rows = db_session.query(PraiseComment).filter(
            PraiseComment.praised == 1,
            PraiseComment.is_valid == 1
        ).all()

        for row in rows:
            print(row.comment_id)
            print(row.praised)


