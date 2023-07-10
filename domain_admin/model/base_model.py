# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

import logging
from logging.handlers import RotatingFileHandler

from peewee import Model
from playhouse.db_url import connect

from domain_admin.config import DB_CONNECT_URL
from domain_admin.service.file_service import resolve_log_file

logger = logging.getLogger('peewee')

# 单个日志文件最大为1M
handler = RotatingFileHandler(
    filename=resolve_log_file("peewee.log"),
    maxBytes=1024 * 1024 * 1,
    encoding='utf-8')

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# 多线程写入方式，会造成读取不到刚写入的数据
db = connect(url=DB_CONNECT_URL)


class BaseModel(Model):
    class Meta:
        database = db
