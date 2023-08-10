import json
import time

from flask import Blueprint, render_template, request, session, make_response, jsonify

from app.config.ue_config import ARTICLE_UECONFIG
from common.response_message import ArticleMessage
from common.utils import compress_image
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
    common_obj = Comment()
    comment_list = common_obj.get_comment_list(aid)
    # comment num
    comment_num = common_obj.get_comment_list_total(aid)
    # print('評論列表:', comment_list)

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
        comment_list=comment_list,
        comment_num=comment_num
    )


@article.route('/article/new')
def article_new():
    # uid = session.get('uid')
    return render_template('new_article.html')


def get_article_request_param(request_data):
    user = User().find_by_uid(session.get('uid'))
    title = request_data.get('title')
    content = request_data.get('content')
    return user, title, content


@article.route('/ue', methods=['GET', 'POST'])
def ueditor():
    param = request.args.get('action')
    if request.method == 'GET' and param == 'config':
        return make_response(ARTICLE_UECONFIG)
    # elif param == 'uploadimage':
    elif param == 'image':
        f = request.files.get('file')
        filename = f.filename
        suffix = filename.split('.')[-1]
        newname = time.strftime('%Y%m%d_%H%M%S.' + suffix)
        f.save('template/upload/' + newname)
        # 壓縮圖片
        source = dest = 'template/upload' + newname
        compress_image(source, dest, 1200)
        # {
        #     "state": "SUCCESS",
        #     "url": "upload/demo.jpg",
        #     "title": "demo.jpg",
        #     "original": "demo.jpg"
        # }
        result = {}
        result['state'] = "SUCCESS"
        result['url'] = '/upload' + newname
        result['title'] = filename
        result['original'] = filename
    return jsonify(result)


@article.route('/article/save', methods=['POST'])
def article_save():
    request_data = json.loads(request.data)
    aid = request_data.get('aid')
    drafted = request_data.get('drafted')

    if aid == -1 and drafted == 0:
        user, title, content, = get_article_request_param(request_data)
        if title == '':
            return ArticleMessage.other('請輸入文章Title')
        aid = Article().insert_article(user.uid, title, content, drafted)
        return ArticleMessage.saved_success(aid)
    elif aid > -1:
        user, title, content, = get_article_request_param(request_data)
        if title == '':
            return ArticleMessage.other('請輸入文章Title')
        label_name = request_data.get('label_name')
        article_tag = request_data.get('article_tag')
        article_type = request_data.get('article_type')

        aid = Article().update_article(aid, title, content, drafted, label_name, article_tag, article_type)
        return ArticleMessage.saved_success(aid)

