import random

from sqlalchemy import Table
from common.database import db_connect

engine, db_session, Base = db_connect()


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

