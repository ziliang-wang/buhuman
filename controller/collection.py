import json

from flask import Blueprint, render_template, request, session, make_response, jsonify

from common.response_message import CollectionMessage
from model.article import Article
from app.config.config import config
from app.settings import env
from model.collection import Collection
from model.notification import Notification
from model.user import User

collect = Blueprint('collect', __name__)


@collect.route('/collect/update', methods=['POST'])
def update_collection_status():
    request_data = json.loads(request.data)
    uid = session.get('uid')
    aid = request_data.get('aid')
    collected = request_data.get('collected')
    collection = Collection()
    tid = Article().get_article_detail(aid).uid
    notification_obj = Notification()

    try:
        collected_num = collection.update_status(uid, aid, collected)
        notification_obj.update_collected_notification(uid, tid, aid, collected)
        return CollectionMessage.success(collected_num)
    except Exception as e:
        return CollectionMessage.fail('收藏失败')


@collect.route('/collect/status', methods=['GET'])
def get_collect_status():
    # request_data = json.loads(request.data)
    uid = session.get('uid')
    aid = request.args.get('aid')
    collection = Collection()
    collected = collection.get_collection_status(uid, aid)

    return {
        'status': 3000,
        'collected': collected
    }
