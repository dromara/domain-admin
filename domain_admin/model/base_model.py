# -*- coding: utf-8 -*-
import logging

from peewee import Model
from playhouse.sqliteq import SqliteQueueDatabase

from domain_admin.config import SQLITE_DATABASE_PATH

# 打印日志
from domain_admin.service.file_service import resolve_log_file

logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler(resolve_log_file("peewee.log")))
logger.setLevel(logging.DEBUG)

# db = connect(SQLITE_DATABASE_URL)
db = SqliteQueueDatabase(database=SQLITE_DATABASE_PATH)


class BaseModel(Model):
    class Meta:
        database = db
