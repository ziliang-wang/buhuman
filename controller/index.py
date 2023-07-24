from flask import Blueprint, render_template, request
from model.article import Article
from app.config.config import config
from app.settings import env

index = Blueprint('index', __name__)

label_types = {
    'recommend': {
        'name': '推薦',
        'selected': 'selected'
    },
    'auto_test': {
        'name': '自動化測試',
        'selected': 'no-selected'
    },
    'python': {
        'name': 'Python開發',
        'selected': 'no-selected'
    },
    'java': {
        'name': 'java開發',
        'selected': 'no-selected'
    },
    'function_test': {
        'name': '功能測試',
        'selected': 'no-selected'
    },
    'perf_test': {
        'name': '性能測試',
        'selected': 'no-selected'
    },
    'funny': {
        'name': '幽默段子',
        'selected': 'no-selected'
    },
}


@index.route('/')
def home():
    page = request.args.get('page', None)
    if not page:
        page = 1

    try:
        page = int(page)
    except Exception as e:
        page = 1

    article_type = request.args.get('type', None)

    if not article_type:
        article_type = 'recommend'

    article = Article()

    total_page = article.calc_total_page(article_type)
    if page > total_page:
        page = 1

    db_result = article.find_article(page, article_type)

    for article, nickname in db_result:
        # article label name
        article.label = label_types.get(article.label_name).get('name')
        # date
        article.create_time = str(article.create_time.month) + '.' + str(article.create_time.day)
        # image path
        article.article_image = config[env].article_header_image_path + str(article.article_image)
        # tag formatter
        article.article_tag = article.article_tag.replace(',', ' · ')

    # left menu category
    for k, v in label_types.items():
        if article_type == k:
            v['selected'] = 'selected'
        else:
            v['selected'] = 'no-selected'

    return render_template(
        'index.html',
        result=db_result,
        total_page=total_page,
        current_page=page,
        label_types=label_types,
        type=article_type
    )
