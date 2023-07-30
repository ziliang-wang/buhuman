import json

from flask import Blueprint, render_template, request, session, make_response, jsonify

from common.response_message import CollectionMessage, PraiseMessage
from model.article import Article
from app.config.config import config
from app.settings import env
from model.collection import Collection
from model.praise import Praise
from model.user import User

praise = Blueprint('praise', __name__)


@praise.route('/praise/update', methods=['POST'])
def update_status():
    request_data = json.loads(request.data)
    uid = session.get('uid')
    aid = request_data.get('aid')
    praised = request_data.get('praised')
    praise_obj = Praise()
    try:
        praised_num = praise_obj.update_status(uid, aid, praised)
        return PraiseMessage.success(praised_num)
    except Exception as e:
        return PraiseMessage.fail('點讚失败')


@praise.route('/praise/status', methods=['GET'])
def get_status():
    # request_data = json.loads(request.data)
    uid = session.get('uid')
    aid = request.args.get('aid')
    praise_obj = Praise()
    praised = praise_obj.get_praise_status(uid, aid)
    praised_num = praise_obj.calc_praised_num(aid)

    return {
        'status': 4000,
        'praised': praised,
        'praisedNum': praised_num
    }
