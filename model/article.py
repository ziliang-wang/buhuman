from sqlalchemy import Table
from common.database import db_connect
from app.config.config import config
from app.settings import env
from model.user import User

engine, db_session, Base = db_connect()


class Article(Base):
    __table__ = Table('article', Base.metadata, autoload_with=engine)

    def calc_total_page(self, article_type):

        if article_type == 'recommend':
            total_rows = db_session.query(Article, User.nickname).join(
                User, User.uid == Article.uid
            ).filter(
                Article.drafted == 1,
                Article.is_valid == 1).all()
            total_page = len(total_rows) // config[env].page_count
        else:
            total_rows = db_session.query(Article, User.nickname).join(
                User, User.uid == Article.uid
            ).filter(
                Article.label_name == article_type,
                Article.drafted == 1,
                Article.is_valid == 1).all()
            total_page = len(total_rows) // config[env].page_count

        return total_page + 1

    def find_article(self, page, article_type='recommend'):
        if page < 1:
            page = 1
        # page = int(page)
        # count = page * config[env].page_count
        count = config[env].page_count

        if article_type == 'recommend':
            result = db_session.query(Article, User.nickname).join(
                User, User.uid == Article.uid
            ).filter(
                # Article.label_name == 'java',
                Article.drafted == 1,
                Article.is_valid == 1).order_by(
                Article.browse_num.desc()
            ).offset((page - 1) * count).limit(count).all()
            # ).limit(count).all()
        else:
            result = db_session.query(Article, User.nickname).join(
                User, User.uid == Article.uid).filter(
                Article.label_name == article_type,
                Article.is_valid == 1,
                Article.drafted == 1
            ).order_by(
                Article.browse_num.desc()
            ).offset((page - 1) * count).limit(count).all()
            # ).limit(count).all()

        return result
