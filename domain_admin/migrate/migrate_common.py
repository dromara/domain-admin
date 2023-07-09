# -*- coding: utf-8 -*-
"""
@File    : migrate_common.py
@Date    : 2023-06-16
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import traceback

from peewee import MySQLDatabase, SqliteDatabase, PostgresqlDatabase
from playhouse.cockroachdb import CockroachDatabase
from playhouse.migrate import (
    MySQLMigrator, SqliteMigrator,
    SchemaMigrator, CockroachDBMigrator,
    PostgresqlMigrator,
    migrate
)

from domain_admin.log import logger


def get_migrator(db):
    """
    不同的数据库，迁移方法不一样
    :param db:
    :return:
    """

    # mysql
    if isinstance(db, MySQLDatabase):
        return MySQLMigrator(db)
    # sqlite
    elif isinstance(db, SqliteDatabase):
        return SqliteMigrator(db)
    # Cockroach
    elif isinstance(db, CockroachDatabase):
        return CockroachDBMigrator(db)
    # Postgresql
    elif isinstance(db, PostgresqlDatabase):
        return PostgresqlMigrator(db)
    else:
        return SchemaMigrator(db)


def try_execute_migrate(migrate_rows):
    """
    执行迁移命令，旧版本可能因为字段缺失而报错
    :param migrate_rows: list
    :return:
    """
    for migrate_row in migrate_rows:
        try:
            migrate(migrate_row)
        except Exception as e:
            logger.error(traceback.format_exc())
