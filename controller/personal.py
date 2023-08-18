import json
import random
import time

from flask import Blueprint, render_template, request, session, make_response, jsonify, url_for

from app.config.ue_config import ARTICLE_UECONFIG
from common.response_message import ArticleMessage, PersonalMessage
from common.utils import compress_image, model_to_json
from model.article import Article
from app.config.config import config
from app.settings import env
from model.collection import Collection
from model.comment import Comment
from model.concern import Concern
from model.user import User

personal = Blueprint('personal', __name__)


@personal.before_request
def personal_before_request():
    url = request.path
    is_login = session.get('is_login')

    if url.startswith('/personal') and is_login != 'true':
        response = make_response('Please Login', 302)
        response.headers['Location'] = url_for('index.home')

        return response


@personal.route('/personal')
def personal_center():
    uid = session.get('uid')

    type_name = request.args.get('type')
    if not type_name:
        type_name = 'article'

    article = Article()
    if type_name == 'article':
        data_list = article.get_article_by_uid(uid)
    elif type_name == 'collection':
        data_list = article.get_collection_article_by_uid(uid)
    elif type_name == 'comment':
        data_list = article.get_comment_article_by_uid(uid)
    elif type_name == 'praise':
        data_list = article.get_praise_article_by_uid(uid)
    else:
        return PersonalMessage.fail('参數傳遞錯誤')

    user = User().find_by_uid(uid)

    # 關注
    concern_num = article.get_concern_num_by_uid(uid)
    # 粉絲
    fans_num = article.get_fans_num_by_uid(uid)
    # 績分
    score = article.get_article_score_by_uid(uid)

    return render_template('personal.html',
                           data_list=data_list,
                           user=user,
                           active=type_name,
                           concern_num=concern_num,
                           fans_num=fans_num,
                           score=score
                           )

