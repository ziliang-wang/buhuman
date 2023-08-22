import random
from sqlalchemy import Table
from common.database import db_connect
engine, db_session, Base = db_connect()
from app.config.config import config
from app.settings import env


class User(Base):
    __table__ = Table('user', Base.metadata, autoload_with=engine)

    def get_one(self):
        return db_session.query(User).first()

    def find_by_username(self, username):
        user_find_result = db_session.query(User).filter(User.username == username).first()
        return user_find_result

    def do_register(self, username, password):
        nickname = username.split('@')[0]
        # avatar
        avatar_num = random.randint(1, 539)
        avatar = str(avatar_num) + '.jpg'
        job = '未定義'
        user = User(
            username=username,
            password=password,
            nickname=nickname,
            avatar=avatar,
            job=job
        )
        db_session.add(user)
        db_session.commit()
        return user

    def find_by_uid(self, uid):

        user_info = db_session.query(User).filter_by(uid=uid).first()

        if user_info.avatar.startswith(config[env].user_avatar_path):
            return user_info
        user_info.avatar = config[env].user_avatar_path + user_info.avatar
        return user_info

    def update_user_header_img(self, uid, filename):
        row = db_session.query(User).filter_by(uid=uid, is_valid=1).first()
        if row:
            row.avatar = filename
        db_session.commit()

    def alter_gender(self, uid, gender):
        row = db_session.query(User).filter_by(uid=uid, is_valid=1).first()
        row.gender = gender
        db_session.commit()

        return row.gender

    def alter_slogan(self, uid, slogan):
        row = db_session.query(User).filter_by(uid=uid, is_valid=1).first()
        row.slogan = slogan
        db_session.commit()

        return row.slogan

    def alter_password(self, uid, password):
        row = db_session.query(User).filter_by(uid=uid, is_valid=1).first()
        row.password = password
        db_session.commit()

        # return row.slogan

    def check_nickname(self, uid, nickname):
        row = db_session.query(User).filter_by(uid=uid, nickname=nickname, is_valid=1).first()
        print('nickname:', nickname)
        if row:
            return True
        return False

    def alter_nickname(self, uid, nickname):
        row = db_session.query(User).filter_by(uid=uid, is_valid=1).first()
        row.nickname = nickname
        db_session.commit()
        return row.nickname
        # print('nickname:', nickname)
        # if row:
        #     return True
        # return False

    def alter_job(self, uid, job):
        row = db_session.query(User).filter_by(uid=uid, is_valid=1).first()
        row.job = job
        db_session.commit()

        return row.job

    def alter_introduce(self, uid, introduce):
        row = db_session.query(User).filter_by(uid=uid, is_valid=1).first()
        row.introduce = introduce
        db_session.commit()

        return row.introduce

    # def get_user_slogan(self, uid):
    #     row = db_session.query(User).filter_by(uid=uid, is_valid=1).first()
    #     return row.slogan
