# -*- coding: utf-8 -*-
import logging

from peewee import Model
from playhouse.sqliteq import SqliteQueueDatabase

from domain_admin.config import SQLITE_DATABASE_PATH

# 打印日志
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# db = connect(SQLITE_DATABASE_URL)
db = SqliteQueueDatabase(database=SQLITE_DATABASE_PATH)


class BaseModel(Model):
    class Meta:
        database = db
