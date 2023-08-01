import json

from flask import Blueprint, render_template, request, session, make_response, jsonify

from common.response_message import CollectionMessage, PraiseMessage, ConcernMessage
from model.article import Article
from app.config.config import config
from app.settings import env
from model.collection import Collection
from model.concern import Concern
from model.praise import Praise
from model.user import User

concern = Blueprint('concern', __name__)


@concern.route('/concern/update', methods=['POST'])
def update_status():
    request_data = json.loads(request.data)
    fid = session.get('uid')
    tid = request_data.get('tid')
    concerned = request_data.get('concerned')
    concern_obj = Concern()
    try:
        concerned_num = concern_obj.update_status(fid, tid, concerned)
        return ConcernMessage.success(concerned_num)
    except Exception as e:
        return ConcernMessage.fail('關注失败')


@concern.route('/concern/status', methods=['GET'])
def get_status():
    # request_data = json.loads(request.data)
    fid = session.get('uid')
    tid = request.args.get('tid')
    concern_obj = Concern()
    concerned = concern_obj.get_concern_status(fid, tid)
    # concerned_num = concern_obj.calc_concerned_num(tid)

    return {
        'status': 5000,
        'concerned': concerned,
        # 'concernedNum': concerned_num
    }
