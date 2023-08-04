from sqlalchemy import Table, or_
from common.database import db_connect
from app.config.config import config
from app.settings import env
from common.utils import model_to_json
from model.collection import Collection
from model.praise import Praise
from model.user import User
from sqlalchemy.sql.functions import sum, count

engine, db_session, Base = db_connect()


class Comment(Base):
    __table__ = Table('comment', Base.metadata, autoload_with=engine)

    # data model
    # final_data_list = [
    #     {
    #         'reply_list': [
    #             {},
    #             {}
    #         ]
    #     },
    #     {},
    #     {}
    # ]

    def get_comment_list(self, aid):
        final_data_list = []
        # 一級評論 帶有樓層的新開評論
        comment_floor_list = self.find_comment_by_aid(aid)
        for comment in comment_floor_list:
            user = User()
            all_reply = self.find_base_by_comment_id(base_reply_id=comment.id)
            # print('all reply:', all_reply)
            comment_user = user.find_by_uid(comment.uid)
            # 每一個回覆的評論
            reply_list = []
            for reply in all_reply:
                # 當前這條評論的所有回覆評論
                reply_content_with_user = {}
                from_user = user.find_by_uid(reply.uid)
                to_user_data = self.find_reply_by_reply_id(reply.reply_id)
                to_user = user.find_by_uid(to_user_data[0].uid)

                reply_content_with_user['from'] = model_to_json(from_user)
                reply_content_with_user['to'] = model_to_json(to_user)
                reply_content_with_user['content'] = model_to_json(reply)
                reply_list.append(reply_content_with_user)

            each_comment_data = model_to_json(comment)
            each_comment_data.update(model_to_json(comment_user))
            each_comment_data['reply_list'] = reply_list

            final_data_list.append(each_comment_data)

        return final_data_list

    def find_comment_by_aid(self, aid):
        result = db_session.query(Comment).filter_by(
            aid=aid,
            base_reply_id=0,
            reply_id=0,
            is_valid=1
        ).order_by(
            Comment.id.desc()
        ).all()

        return result

    def find_base_by_comment_id(self, base_reply_id):
        result = db_session.query(Comment).filter_by(
            base_reply_id=base_reply_id,
            is_valid=1
        ).order_by(
            Comment.id.desc()
        ).all()

        return result

    def find_reply_by_reply_id(self, reply_id):
        result = db_session.query(Comment).filter_by(
            id=reply_id,
            is_valid=1
        ).order_by(
            Comment.id.desc()
        ).all()

        return result