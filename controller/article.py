from flask import Blueprint, render_template, request
from model.article import Article
from app.config.config import config
from app.settings import env

index = Blueprint('index', __name__)