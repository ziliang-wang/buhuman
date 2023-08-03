from flask import Blueprint, render_template, request, session
from model.article import Article
from app.config.config import config
from app.settings import env
from model.collection import Collection
from model.comment import Comment
from model.concern import Concern
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
    collection_and_praise = article.get_collection_and_praise(user_info.uid)
    # 作者粉絲數
    concern_obj = Concern()
    fans_num = concern_obj.calc_concerned_num(tid=article_content.uid)
    # print(fans_num)
    # comment
    comment_list = Comment().get_comment_list(aid)
    print('評論列表:', comment_list)

    return render_template(
        'article-detail.html',
        article=article_content,
        user=user_info,
        # is_collected=is_collected,
        tags_list=tags_list,
        relation_list=relation_list,
        user_articles=user_articles,
        collection_and_praise=collection_and_praise,
        fans_num=fans_num,
        comment_list=comment_list
    )
