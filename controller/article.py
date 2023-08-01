from flask import Blueprint, render_template, request, session
from model.article import Article
from app.config.config import config
from app.settings import env
from model.collection import Collection
from model.user import User

article = Blueprint('article', __name__)


@article.route('/detail')
def article_detail():
    aid = request.args.get('aid')
    article = Article()
    article_content = article.get_article_detail(aid)
    tags_list = article_content.article_tag.split(',')
    user = User()
    user_info = user.find_by_uid(article_content.uid)

    # relation_list = article.get_relation_articles(article_content.label_name)
    relation_list = article.get_relation_articles(tags_list)
    # print('author uid', user_info.uid)
    # 作者文章數
    user_articles = article.get_user_articles(user_info.uid)
    # 獲讚與點讚
    # collection_and_praise = article.get_collection_and_praise(aid)


    # todo 查看評論的信息
    # todo 文章收藏數量
    # todo "我"是否收藏
    # is_collected 取自db
    # is_collected = 1
    #
    # if session.get('is_login') == 'true':
    #     uid = session.get('uid')
    #     is_collected = Collection().get_collection_status(uid, article_content.aid)

    return render_template(
        'article-detail.html',
        article=article_content,
        user=user_info,
        # is_collected=is_collected,
        tags_list=tags_list,
        relation_list=relation_list,
        user_articles=user_articles
        # collection_and_praise=collection_and_praise
    )
