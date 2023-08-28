import json

from flask import Blueprint, render_template, request, session, make_response, jsonify

from common.response_message import CollectionMessage, PraiseMessage
from model.article import Article
from app.config.config import config
from app.settings import env
from model.collection import Collection
# from model.praise import Praise
from model.praise_comment import PraiseComment
from model.user import User

praise_comment = Blueprint('praise_comment', __name__)


@praise_comment.route('/praise/comment/update', methods=['POST'])
def update_status():
    request_data = json.loads(request.data)
    uid = session.get('uid')
    comment_id = request_data.get('cid')
    praised = request_data.get('praised')
    praise_obj = PraiseComment()
    try:
        praised_num = praise_obj.update_status(uid, comment_id, praised)
        return PraiseMessage.success(praised_num)
    except Exception as e:
        return PraiseMessage.fail('點讚失败')


@praise_comment.route('/praise/comment/status', methods=['GET'])
def get_status():
    # request_data = json.loads(request.data)
    uid = session.get('uid')
    cid = int(request.args.get('cid'))

    # print(comment_id)

    praise_obj = PraiseComment()
    praised = praise_obj.get_praise_status(uid, cid)
    praised_num = praise_obj.calc_praised_num(cid)
    # praise_obj.get_all_praise_comment()
    # print(praised_num)

    return {
        'status': 4000,
        'praised': praised,
        'praisedNum': praised_num
    }
