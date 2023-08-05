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