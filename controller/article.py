from flask import Blueprint, render_template, request
from model.article import Article
from app.config.config import config
from app.settings import env
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
    # todo 查看評論的信息
    # todo 文章收藏數量
    # todo "我"是否收藏
    is_collected = 0
    return render_template(
        'article-detail.html',
        article=article_content,
        user=user_info,
        collected=is_collected,
        tags_list=tags_list
    )
