import json
import time

from flask import Blueprint, render_template, request, session, make_response, jsonify

from app.config.ue_config import FEEDBACK_UECONFIG
from common.response_message import CollectionMessage, PraiseMessage, ConcernMessage
from common.utils import compress_image
from model.article import Article
from app.config.config import config
from app.settings import env
from model.collection import Collection
from model.concern import Concern
from model.praise import Praise
from model.user import User

comment = Blueprint('comment', __name__)


@comment.route('/comment', methods=['GET', 'POST'])
def publish_comment():
    param = request.args.get('action')
    if request.method == 'GET' and param == 'config':
        return make_response(FEEDBACK_UECONFIG)
    elif param == 'uploadimage':
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
