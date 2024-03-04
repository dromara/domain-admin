# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
import logging
from logging.handlers import RotatingFileHandler

from domain_admin.service.file_service import resolve_log_file
from domain_admin.config import APP_MODE

logger = logging.getLogger('domain-admin')

# 单个日志文件最大为1M
handler = RotatingFileHandler(
    filename=resolve_log_file("domain-admin.log"),
    backupCount=1,
    maxBytes=1024 * 1024 * 1,
    encoding='utf-8'
)

# 设置日志格式
formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s] %(filename)s/%(funcName)s:\n%(message)s\n',
    datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

# logger.addHandler(logging.FileHandler(resolve_log_file("domain-admin.log")))
logger.addHandler(handler)
logger.setLevel(logging.ERROR)

# development
if APP_MODE == 'development':
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
