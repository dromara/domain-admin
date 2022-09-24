# -*- coding: utf-8 -*-
from peewee import Model
from playhouse.db_url import connect

from domain_admin.config import SQLITE_DATABASE_URL

import logging

# 打印日志
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

db = connect(SQLITE_DATABASE_URL)


class BaseModel(Model):
    class Meta:
        database = db
