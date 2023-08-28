import os
from flask import Flask

from controller.article import article
from controller.comment import comment
from controller.concern import concern
from controller.index import index
from controller.personal import personal
from controller.praise import praise
from controller.praise_comment import praise_comment
from controller.user import user
from controller.collection import collect


def create_app():
    app = Flask(__name__, template_folder='../template', static_url_path='/', static_folder='../template')
    app.config['SECRET_KEY'] = os.urandom(24)
    init_blueprint(app)

    return app


def init_blueprint(app):
    app.register_blueprint(user)
    app.register_blueprint(index)
    app.register_blueprint(article)
    app.register_blueprint(collect)
    app.register_blueprint(praise)
    app.register_blueprint(concern)
    app.register_blueprint(comment)
    app.register_blueprint(personal)
    app.register_blueprint(praise_comment)
