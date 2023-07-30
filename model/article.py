from sqlalchemy import Table, or_
from common.database import db_connect
from app.config.config import config
from app.settings import env
from model.user import User

engine, db_session, Base = db_connect()


class Article(Base):
    __table__ = Table('article', Base.metadata, autoload_with=engine)

    def calc_search_total_page(self, keyword):

        count = config[env].page_count

        if keyword:
            search_total_rows = db_session.query(Article, User.nickname).join(
                User, User.uid == Article.uid).filter(
                or_(
                    Article.title.like('%' + keyword + '%'),
                    Article.article_content.like('%' + keyword + '%')
                ),
                Article.is_valid == 1,
                Article.drafted == 1
            ).all()

            search_total_page = len(search_total_rows) // count
            # print('search rows:', keyword, len(search_total_rows))
        else:
            search_total_rows = []
            search_total_page = 0

        return search_total_page + 1, search_total_rows

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

        return total_page + 1, total_rows

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

    def search_article(self, page, keyword):
        if page < 1:
            page = 1
        count = config[env].page_count

        result = db_session.query(Article, User.nickname).join(
            User, User.uid == Article.uid).filter(
            or_(
                Article.title.like('%' + keyword + '%'),
                Article.article_content.like('%' + keyword + '%')
            ),
            Article.is_valid == 1,
            Article.drafted == 1
        ).order_by(
            Article.browse_num.desc()
        ).offset((page - 1) * count).limit(count).all()

        return result

    def get_article_detail(self, aid):
        row = db_session.query(Article).filter_by(aid=aid).first()
        row.browse_num += 1
        db_session.commit()
        return row

    # def get_relation_articles(self, label_name):
    #     result = db_session.query(Article).filter_by(label_name=label_name).order_by(
    #         Article.browse_num.desc()
    #     ).limit(5).all()
    #     return result

    def get_relation_articles(self, tag_list):
        result_list = []
        for tag_name in tag_list:
            row = db_session.query(Article).filter(
                or_(Article.article_tag == tag_name)
            ).order_by(
                Article.browse_num.desc()
            ).all()

            result_list.append(row)

        print(result_list)

        return result_list[0][:5]
