import json

from flask import Blueprint, render_template, request, session

from common.response_message import CollectionMessage
from model.article import Article
from app.config.config import config
from app.settings import env
from model.collection import Collection
from model.user import User

collect = Blueprint('collect', __name__)


@collect.route('/collect/update', method=['POST'])
def update_collection_status():
    request_data = json.loads(request.data)
    uid = session.get('uid')
    aid = request_data.get('aid')
    collected = request_data.get('collected')
    collection = Collection()
    try:
        collection.update_status(uid, aid, collected)
        return CollectionMessage.success('收藏成功')
    except Exception as e:
        return CollectionMessage.fail('收藏失败')
