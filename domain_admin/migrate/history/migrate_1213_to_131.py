# -*- coding: utf-8 -*-
"""
@File    : migrate_1213_to_131.py
@Date    : 2023-06-03

cmd:
$ python domain_admin/migrate/migrate_1213_to_131.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from playhouse.migrate import SqliteMigrator, migrate

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel


def execute_migrate():
    """
    版本升级 1.2.13 => 1.3.1
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        migrator.add_column(DomainModel._meta.table_name, DomainModel.port.name, DomainModel.port),
        migrator.add_column(DomainModel._meta.table_name, DomainModel.domain_expire_monitor.name, DomainModel.domain_expire_monitor),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
