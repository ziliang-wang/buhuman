from flask import Flask


def create_app():
    app = Flask(__name__, template_folder='../template', static_url_path='/', static_folder='../template')
    return app