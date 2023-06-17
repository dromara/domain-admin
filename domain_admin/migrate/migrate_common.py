# -*- coding: utf-8 -*-
"""
@File    : migrate_common.py
@Date    : 2023-06-16
"""
from peewee import MySQLDatabase, SqliteDatabase, PostgresqlDatabase
from playhouse.cockroachdb import CockroachDatabase
from playhouse.migrate import MySQLMigrator, SqliteMigrator, SchemaMigrator, CockroachDBMigrator, PostgresqlMigrator


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
