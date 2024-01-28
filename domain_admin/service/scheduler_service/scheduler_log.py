# -*- coding: utf-8 -*-
"""
@File    : scheduler_log.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""

from __future__ import print_function, unicode_literals, absolute_import, division

import logging
import warnings
from logging.handlers import RotatingFileHandler

from domain_admin.config import APP_MODE
from domain_admin.service.file_service import resolve_log_file

warnings.filterwarnings(action="ignore")


def init_log():
    apscheduler_logger = logging.getLogger('apscheduler')

    # 单个日志文件最大为1M
    handler = RotatingFileHandler(
        filename=resolve_log_file("apscheduler.log"),
        maxBytes=1024 * 1024 * 1,
        backupCount=1,
        encoding='utf-8'
    )

    # 设置日志格式
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    apscheduler_logger.addHandler(handler)

    apscheduler_logger.setLevel(logging.ERROR)

    # development
    if APP_MODE == 'development':
        apscheduler_logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        apscheduler_logger.addHandler(stream_handler)
