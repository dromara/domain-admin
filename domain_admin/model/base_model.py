# -*- coding: utf-8 -*-
from peewee import Model
from playhouse.db_url import connect
# from playhouse.signals import Model, pre_save
from playhouse.sqliteq import SqliteQueueDatabase

from domain_admin.config import SQLITE_DATABASE_URL, SQLITE_DATABASE_PATH

import logging

# 打印日志
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# db = connect(SQLITE_DATABASE_URL)
db = SqliteQueueDatabase(database=SQLITE_DATABASE_PATH)


class BaseModel(Model):
    class Meta:
        database = db