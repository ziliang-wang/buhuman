from sqlalchemy import Table, or_
from common.database import db_connect
from app.config.config import config
from app.settings import env
from model.collection import Collection
from model.comment import Comment
from model.concern import Concern
from model.praise import Praise
from model.user import User
from sqlalchemy.sql.functions import sum, count

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
        row = db_session.query(Article).filter_by(aid=aid, drafted=1, is_valid=1).first()
        if row:
            row.browse_num += 1
            db_session.commit()
        return row

    # def get_relation_articles(self, label_name):
    #     result = db_session.query(Article).filter_by(label_name=label_name).order_by(
    #         Article.browse_num.desc()
    #     ).limit(5).all()
    #     return result

    def get_relation_articles(self, tag_list):
        result_list = set()

        rows = db_session.query(Article).filter_by(
            drafted=1,
            is_valid=1
        ).order_by(
            Article.browse_num.desc()
        ).all()

        for row in rows:
            if row.article_tag.split(','):
                row_tag = row.article_tag.split(',')
                for tag_name in tag_list:
                    if tag_name in row_tag:
                        result_list.add(row)

        return list(result_list)[:5]

    def get_user_articles(self, uid):
        user_articles = db_session.query(count(Article.uid)).filter_by(uid=uid, drafted=1, is_valid=1).first()
        # print(user_articles)
        if not user_articles:
            return 0
        # print(user_articles)
        return user_articles[0]

    def get_collection_and_praise(self, uid):
        collection = db_session.query(count(Article.uid)).join(
            Collection, Article.aid == Collection.aid).filter(
            Article.uid == uid,
            Article.drafted == 1,
            Article.is_valid == 1,
            Collection.collected == 1,
            Collection.is_valid == 1
        ).first()

        praise = db_session.query(count(Article.uid)).join(
            Praise, Article.aid == Praise.aid).filter(
            Article.uid == uid,
            Article.drafted == 1,
            Article.is_valid == 1,
            Praise.praised == 1,
            Praise.is_valid == 1
        ).first()

        collection_result = 0
        praise_result = 0

        if collection:
            collection_result = collection[0] or 0

        if praise:
            praise_result = praise[0] or 0

        result = collection_result + praise_result

        return result

    def insert_article(self, uid, title, content, drafted):
        article = Article(
            uid=uid,
            title=title,
            article_content=content,
            drafted=drafted
        )

        db_session.add(article)
        db_session.commit()

        return article.aid

    def update_article(self,
                       aid,
                       title,
                       content,
                       drafted,
                       label_name='',
                       article_tag='',
                       article_type=''
                       ):

        row = db_session.query(Article).filter_by(aid=aid).first()
        row.title = title
        row.article_content = content
        row.drafted = drafted
        row.label_name = label_name
        row.article_tag = article_tag
        row.article_type = article_type

        db_session.commit()

        return aid

    def update_article_header_img(self, aid, filename):
        row = db_session.query(Article).filter_by(aid=aid, is_valid=1).first()
        if row:
            row.article_image = filename
        db_session.commit()

    def get_all_drafted(self, uid):
        result = db_session.query(Article).filter_by(uid=uid, drafted=0, is_valid=1).all()
        return result

    def get_one_drafted(self, aid):
        result = db_session.query(Article).filter_by(aid=aid, drafted=0, is_valid=1).first()
        return result

    def remove_one_drafted(self, aid):
        row = db_session.query(Article).filter_by(aid=aid, drafted=0, is_valid=1).first()
        row.is_valid = 0
        db_session.commit()

    def get_article_by_uid(self, uid):
        # 當前用戶寫了哪些文章
        rows = db_session.query(Article).filter_by(
            uid=uid,
            drafted=1,
            is_valid=1
        ).order_by(
            Article.create_time.desc()
        ).all()

        return self.add_article_image_path(rows)

    def get_collection_article_by_uid(self, uid):
        # 當前用戶，收藏了哪些文章
        rows = db_session.query(Article).join(
            Collection, Article.aid == Collection.aid
        ).filter(
            Collection.uid == uid,
            Collection.collected == 1,
            Collection.is_valid == 1,
            Article.is_valid == 1
        ).order_by(
            Collection.create_time.desc()
        ).all()

        return self.add_article_image_path(rows)

    def get_comment_article_by_uid(self, uid):
        # 當前用戶，評論了哪些文章 我的评论
        rows = db_session.query(Article).join(
            Comment, Article.aid == Comment.aid
        ).filter(
            Comment.uid == uid,
            Comment.floor_number != 0,
            Comment.is_valid == 1,
            Article.is_valid == 1
        ).order_by(
            Comment.create_time.desc()
        ).all()

        return self.add_article_image_path(rows)

    def get_praise_article_by_uid(self, uid):
        # 我的推荐
        rows = db_session.query(Article).join(
            Praise, Article.aid == Praise.aid
        ).filter(
            Praise.uid == uid,
            Praise.praised == 1,
            Praise.is_valid == 1,
            Article.is_valid == 1
        ).order_by(
            Praise.create_time.desc()
        ).all()

        return self.add_article_image_path(rows)

    def add_article_image_path(self, rows):
        if not rows :
            return None

        for row in rows:
            if not row.article_image:
                row.article_image = '1.jpg'
            row.article_image = config[env].article_header_image_path + row.article_image

        return rows

    # 關注
    def get_concern_num_by_uid(self, uid):
        concern_num = db_session.query(Concern).filter(
            Concern.fid == uid,
            Concern.is_valid == 1
        ).count()

        return concern_num

    # 粉絲數
    def get_fans_num_by_uid(self, uid):
        fans_num = db_session.query(Concern).filter(
            Concern.tid == uid,
            Concern.is_valid == 1
        ).count()

        return fans_num

    # 績分
    def get_article_score_by_uid(self, uid):
        score = db_session.query(Article).filter(
            Article.uid == uid,
            Article.is_valid == 1,
            Article.drafted == 1
        ).count()

        return score

    def remove_article(self, uid, aid):
        row = db_session.query(Article).filter(
            Article.uid == uid,
            Article.aid == aid,
            Article.is_valid == 1,
            Article.drafted == 1
        ).first()

        if row:
            praise_row = db_session.query(Praise).filter(
                Praise.aid == aid,
                Praise.praised == 1
            ).first()

            collection_row = db_session.query(Collection).filter(
                Collection.aid == aid,
                Collection.collected == 1
            ).first()

            if praise_row:
                praise_row.is_valid = 0

            if collection_row:
                collection_row.collected = 0

            row.is_valid = 0
            db_session.commit()
            return True
        return False

    def get_article_list_by_uid(self, uid):
        rows = db_session.query(Article).filter(
            Article.uid == uid,
            Article.drafted == 1,
            Article.is_valid == 1
        ).order_by(
            Article.create_time.desc()
        ).all()

        return rows



