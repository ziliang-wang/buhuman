import json
import random
import time

from flask import Blueprint, render_template, request, session, make_response, jsonify, url_for

from app.config.ue_config import ARTICLE_UECONFIG
from common.response_message import ArticleMessage
from common.utils import compress_image, model_to_json
from model.article import Article
from app.config.config import config
from app.settings import env
from model.collection import Collection
from model.comment import Comment
from model.concern import Concern
from model.user import User

article = Blueprint('article', __name__)
label_types = config[env].label_types
article_types = config[env].article_types


@article.before_request
def article_before_request():
    url = request.path
    is_login = session.get('is_login')

    if url.startswith('/article/new') and is_login != 'true':
        response = make_response('Please Login', 302)
        response.headers['Location'] = url_for('index.home')

        return response


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
    uid = session.get('uid')
    all_drafted = Article().get_all_drafted(uid)
    drafted_num = 0
    if all_drafted:
        drafted_num = len(all_drafted)

    return render_template('new_article.html',
                           label_types=label_types,
                           article_types=article_types,
                           all_drafted=all_drafted,
                           drafted_count=drafted_num
                           )


@article.route('/article/drafted', methods=['POST'])
def get_drafted_detail():
    request_data = json.loads(request.data)
    aid = request_data.get('aid')
    result = Article().get_one_drafted(aid=aid)
    article_drafted_detail = model_to_json(result)

    return ArticleMessage.success(article_drafted_detail)


@article.route('/article/remove/draft', methods=['POST'])
def remove_drafted():
    uid = session.get('uid')
    if request.method == 'POST':
        request_data = json.loads(request.data)
        aid = request_data.get('aid')
        Article().remove_one_drafted(aid=aid)
        all_drafted = Article().get_all_drafted(uid)
        drafted_num = 0
        if all_drafted:
            drafted_num = len(all_drafted)
        return ArticleMessage.success(drafted_num)


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
    # elif param == 'uploadimage':
    elif param == 'image':
        f = request.files.get('file')
        filename = f.filename
        suffix = filename.split('.')[-1]
        newname = time.strftime('%Y%m%d_%H%M%S.' + suffix)
        f.save('template/upload/' + newname)
        # 壓縮圖片
        source = dest = 'template/upload/' + newname
        compress_image(source, dest, 1200)
        # {
        #     "state": "SUCCESS",
        #     "url": "upload/demo.jpg",
        #     "title": "demo.jpg",
        #     "original": "demo.jpg"
        # }
        result = {}
        result['state'] = "SUCCESS"
        result['url'] = '/upload/' + newname
        # result['title'] = filename
        result['title'] = newname
        # result['original'] = filename
        result['original'] = newname
    return jsonify(result)


@article.route('/article/draft/list')
def get_draft_list():
    uid = session.get('uid')
    drafted_list = []
    all_drafted = Article().get_all_drafted(uid)

    if all_drafted:
        for drafted in all_drafted:
            drafted_list.append(model_to_json(drafted))
        return drafted_list
    return ''


@article.route('/article/save', methods=['POST'])
def article_save():
    request_data = json.loads(request.data)
    aid = request_data.get('aid')
    drafted = request_data.get('drafted')
    uid = session.get('uid')
    drafted_list = []

    if aid == -1 and drafted == 0:
        user, title, content, = get_article_request_param(request_data)
        if title == '':
            return ArticleMessage.other('請輸入文章Title')
        aid = Article().insert_article(user.uid, title, content, drafted)

        all_drafted = Article().get_all_drafted(uid)

        for drafted in all_drafted:
            drafted_list.append(model_to_json(drafted))

        return ArticleMessage.saved_success(len(all_drafted), aid, drafted_list)
    # elif aid > -1 and drafted == 0:
    #     user, title, content, = get_article_request_param(request_data)
    #     if title == '':
    #         return ArticleMessage.other('請輸入文章Title')
    #     label_name = request_data.get('article_label')
    #     article_tag = request_data.get('article_tag')
    #     article_type = request_data.get('article_type')
    #
    #     # uid = session.get('uid')
    #     all_drafted = Article().get_all_drafted(uid)
    #
    #     for drafted in all_drafted:
    #         drafted_list.append(model_to_json(drafted))
    #
    #     aid = Article().update_article(aid, title, content, drafted, label_name, article_tag, article_type)
    #     return ArticleMessage.saved_success(len(all_drafted), aid, drafted_list)
    elif aid > -1:
        user, title, content, = get_article_request_param(request_data)
        if title == '':
            return ArticleMessage.other('請輸入文章Title')
        label_name = request_data.get('article_label')
        article_tag = request_data.get('article_tag')
        article_type = request_data.get('article_type')

        # uid = session.get('uid')
        aid = Article().update_article(aid, title, content, drafted, label_name, article_tag, article_type)

        all_drafted = Article().get_all_drafted(uid)

        for drafted in all_drafted:
            drafted_list.append(model_to_json(drafted))

        return ArticleMessage.saved_success(len(all_drafted), aid, drafted_list)

    return ''


@article.route('/article/upload/cover', methods=['POST'])
def upload_cover_image():
    f = request.files.get('article-header-image')
    filename = f.filename
    suffix = filename.split('.')[-1]
    newname = time.strftime('%Y%m%d_%H%M%S.' + suffix)
    newname = 'article-header-' + newname

    f.save('template/upload/article-header/' + newname)
    # 壓縮圖片
    source = dest = 'template/upload/article-header/' + newname
    compress_image(source, dest, 1200)
    # update database
    aid = request.form.get('aid')
    Article().update_article_header_img(aid, newname)

    result = {}
    result['state'] = "SUCCESS"
    result['url'] = '/upload/article-header/' + newname
    result['title'] = filename
    result['original'] = filename
    return jsonify(result)


@article.route('/article/upload/random', methods=['POST'])
def upload_random_header_image():

    name = random.randint(1, 539)
    newname = str(name) + '.jpg'

    aid = request.form.get('aid')
    Article().update_article_header_img(aid, newname)

    result = {}
    result['state'] = "SUCCESS"
    result['url'] = '/images/headers/' + newname
    result['title'] = newname
    result['original'] = newname
    return jsonify(result)
