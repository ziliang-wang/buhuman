import logging
from logging.handlers import RotatingFileHandler
from app.config.config import config
from app.settings import env
# 增加log的配置


def set_log():
    config_calss = config[env]
    # 設置log的等級
    logging.basicConfig(level=config_calss.LOG_LEVEL)
    # 創建log記錄器
    file_log_handler = RotatingFileHandler('log/buhuman.log', maxBytes=1024*1024*300, backupCount=10)
    # 創建log記錄的格式
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d %(message)s')
    file_log_handler.setFormatter(formatter)
    # 為全域的日誌工具對象添加日誌記錄器
    logging.getLogger().addHandler(file_log_handler)


set_log()
