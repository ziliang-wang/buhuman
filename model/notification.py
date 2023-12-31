from sqlalchemy import Table, or_
from sqlalchemy.ext.hybrid import hybrid_property

from common.database import db_connect
from app.config.config import config
from app.settings import env
from model.concern import Concern
# from model.article import Article
from model.user import User

engine, db_session, Base = db_connect()


class Notification(Base):
    __table__ = Table('notification', Base.metadata, autoload_with=engine)

    def update_comment_notification(self, uid, tid, aid):

        notification = Notification(
            uid=uid,
            tid=tid,
            aid=aid,
            collected=0,
            concerned=0,
            praised=0,
            comment=1
        )
        db_session.add(notification)
        db_session.commit()

    def update_praised_notification(self, uid, tid, aid, praised=0):
        notification_row = db_session.query(Notification).filter_by(
            uid=uid,
            aid=aid,
            collected=0,
            concerned=0,
            comment=0,
            is_valid=1
        ).first()

        if not notification_row:
            notification = Notification(
                uid=uid,
                tid=tid,
                aid=aid,
                collected=0,
                concerned=0,
                comment=0,
                praised=praised
            )
            db_session.add(notification)
        else:
            notification_row.praised = praised

        db_session.commit()

    def update_collected_notification(self, uid, tid, aid, collected=0):
        notification_row = db_session.query(Notification).filter_by(
            uid=uid,
            aid=aid,
            praised=0,
            concerned=0,
            comment=0,
            is_valid=1
        ).first()

        if not notification_row:
            notification = Notification(
                uid=uid,
                tid=tid,
                aid=aid,
                praised=0,
                concerned=0,
                comment=0,
                collected=collected
            )
            db_session.add(notification)
        else:
            notification_row.collected = collected

        db_session.commit()

    def update_concerned_notification(self, uid, tid, concerned=0):
        notification_row = db_session.query(Notification).filter_by(
            uid=uid,
            praised=0,
            collected=0,
            comment=0,
            is_valid=1
        ).first()

        if not notification_row:
            notification = Notification(
                uid=uid,
                tid=tid,
                aid=0,
                praised=0,
                collected=0,
                comment=0,
                concerned=concerned
            )
            db_session.add(notification)
        else:
            notification_row.concerned = concerned

        db_session.commit()

    # fid = 0

    def update_fans_notification(self, uid, caid):
        # concern = Concern()
        # row = db_session.query(Concern).filter_by(tid=uid, concerned=1, is_valid=1).first()
        rows = db_session.query(Concern).filter_by(tid=uid, concerned=1, is_valid=1).all()
        if rows:
            for row in rows:
                fid = row.fid
                # print('fid:', fid)
                notification = Notification(
                    uid=uid,
                    tid=fid,
                    aid=0,
                    caid=caid,
                    collected=0,
                    praised=0,
                    comment=0,
                    concerned=0
                )

                db_session.add(notification)
                db_session.commit()
            return rows
        return None

    def get_notification_list(self, uid):

        from model.article import Article

        result_list = []

        rows = db_session.query(Notification).filter_by(
            tid=uid,
            is_valid=1
        ).order_by(
            Notification.create_time.desc()
        ).limit(10).all()

        for row in rows:
            data = {}
            if not row.concerned:
                data['uid'] = row.uid
                data['nickname'] = User().find_by_uid(row.uid).nickname
                data['avatar'] = User().find_by_uid(row.uid).avatar
                # data['article_avatar'] = Article().get_article_image(row.aid) or Article().get_article_image(row.caid)
                data['article_avatar'] = Article().get_article_image(row.aid) if row.caid == 0 else Article().get_article_image(row.caid)
                # data['aid'] = row.aid or row.caid
                data['aid'] = row.aid if row.caid == 0 else row.caid
                data['praised'] = row.praised
                data['is_read'] = row.is_read
                data['create_time'] = row.create_time
            else:
                data['uid'] = row.uid
                data['nickname'] = User().find_by_uid(row.uid).nickname
                data['avatar'] = User().find_by_uid(row.uid).avatar
                data['aid'] = row.aid
                data['praised'] = row.praised
                data['is_read'] = row.is_read
                data['create_time'] = row.create_time

            if row.praised:
                data['type'] = '讚'
            elif row.collected:
                data['type'] = '收藏'
            elif row.comment:
                data['type'] = '評論'
            elif row.concerned:
                data['type'] = 'concerned'
            elif row.caid:
                data['type'] = 'fans'

            result_list.append(data)
        # fans
        # fans_rows = db_session.query(Notification).filter(
        #     Notification.tid == self.fid,
        #     # Notification.tid == uid,
        #     Notification.caid != 0,
        #     Notification.is_valid == 1
        # ).order_by(
        #     Notification.create_time.desc()
        # ).limit(10).all()

        # for row in fans_rows:
        #     # print('fans', row)
        #     data = {}
        #     data['uid'] = row.uid
        #     data['nickname'] = User().find_by_uid(row.uid).nickname
        #     data['avatar'] = User().find_by_uid(row.uid).avatar
        #     data['aid'] = row.caid
        #     data['praised'] = row.praised
        #     data['is_read'] = row.is_read
        #     data['create_time'] = row.create_time
        #
        #     if row.praised:
        #         data['type'] = '讚'
        #     elif row.collected:
        #         data['type'] = '收藏'
        #     elif row.comment:
        #         data['type'] = '評論'
        #     elif row.concerned:
        #         data['type'] = 'concerned'
        #     elif row.caid:
        #         data['type'] = 'fans'
        #
        #     result_list.append(data)

        # print(result_list)

        return result_list
