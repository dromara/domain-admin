# -*- coding: utf-8 -*-
"""
@File    : migrate_1212_to_1213.py
@Date    : 2023-02-06

cmd:
$ python domain_admin/migrate/migrate_110_to_1212.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from playhouse.migrate import SqliteMigrator, migrate

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel


def execute_migrate():
    """
    版本升级 1.2.12 => 1.2.13
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        migrator.add_column(DomainModel._meta.table_name, DomainModel.domain_auto_update.name, DomainModel.domain_auto_update),
        migrator.add_column(DomainModel._meta.table_name, DomainModel.auto_update.name, DomainModel.auto_update),
        migrator.add_column(DomainModel._meta.table_name, DomainModel.ip_auto_update.name, DomainModel.ip_auto_update),
    ]

    migrate_common.try_execute_migrate(migrate_rows)