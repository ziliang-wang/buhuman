import json
import time

from flask import Blueprint, render_template, request, session, make_response, jsonify

from app.config.ue_config import FEEDBACK_UECONFIG
from common.response_message import CollectionMessage, PraiseMessage, ConcernMessage, CommentMessage
from common.utils import compress_image, model_to_json
from model.article import Article
from app.config.config import config
from app.settings import env
from model.collection import Collection
from model.comment import Comment
from model.concern import Concern
from model.praise import Praise
from model.user import User

comment = Blueprint('comment', __name__)


@comment.route('/comment', methods=['GET', 'POST'])
def ueditor():
    param = request.args.get('action')
    if request.method == 'GET' and param == 'config':
        return make_response(FEEDBACK_UECONFIG)
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


@comment.route('/comment/add', methods=['POST'])
def add_comment():
    request_data = json.loads(request.data)
    aid = request_data.get('aid')
    content = request_data.get('content').strip()
    ipaddr = request.remote_addr
    uid = session.get('uid')

    if len(content) < 5 or len(content) > 1000:
        return CommentMessage.other('內容太長或太短')

    comment = Comment()

    try:
        result = comment.insert_comment(uid, aid, content, ipaddr)
        result = model_to_json(result)
        return CommentMessage.success(result)
    except Exception as e:
        print(e)
        return CommentMessage.fail('failed')


@comment.route('/comment/reply', methods=['POST'])
def reply():
    request_data = json.loads(request.data)
    aid = request_data.get('aid')
    content = request_data.get('content').strip()
    ipaddr = request.remote_addr
    uid = session.get('uid')
    base_reply_id = request_data.get('baseReplyId')
    reply_id = request_data.get('commentReplyId')


    if len(content) < 5 or len(content) > 1000:
        return CommentMessage.other('內容太長或太短')

    comment = Comment()

    try:
        result = comment.insert_reply(uid, aid, base_reply_id, reply_id, content, ipaddr)
        result = model_to_json(result)
        return CommentMessage.success(result)
    except Exception as e:
        print(e)
        return CommentMessage.fail('failed')

