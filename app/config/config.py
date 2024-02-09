# coding: utf-8

# Global Settings

class Config(object):
    db_url = 'mysql+pymysql://root:sys12091%@127.0.0.1:3306/blr1'
    page_count = 10
    article_header_image_path = '/images/article/header/'
    user_avatar_path = '/images/headers/'
    sender = '550310889@qq.com'
    auth_code = 'ndviaaqistysbeae'

    label_types = {
        'default': {
            'name': '請選擇您的文章分類',
            'selected': 'selected'
        },
        'recommend': {
            'name': '推薦',
            'selected': 'no-selected'
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

    article_types = {
        'default': {
            'name': '請選擇',
            'selected': 'selected'
        },
        'first': {
            'name': '首發',
            'selected': 'no-selected'
        },
        'original': {
            'name': '原創',
            'selected': 'no-selected'
        },
        'share': {
            'name': '分享',
            'selected': 'no-selected'
        },
        'recommend': {
            'name': '推薦',
            'selected': 'no-selected'
        },
        'other': {
            'name': '其它',
            'selected': 'no-selected'
        }
    }


# Env settings


class TestConfig(Config):
    is_echo = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    is_echo = False
    LOG_LEVEL = 'INFO'


config = {
    'test': TestConfig,
    'production': ProductionConfig
}
