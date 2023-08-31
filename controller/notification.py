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

notification = Blueprint('notification', __name__)


@notification.route('/notification/remove')
def notification_remove():
    pass