# coding: utf-8

# Global Settings

class Config(object):
    db_url = 'mysql+pymysql://root:sys12091@127.0.0.1:3306/blr1'
    page_count = 10
    article_header_image_path = '/images/article/header/'
    user_avatar_path = '/images/headers/'
    sender = '550310889@qq.com'
    auth_code = 'ndviaaqistysbeae'
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