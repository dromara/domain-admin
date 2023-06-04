# -*- coding: utf-8 -*-
"""
@File    : migrate_1213_to_131.py
@Date    : 2023-06-03

cmd:
$ python domain_admin/migrate/migrate_1213_to_131.py
"""

from playhouse.migrate import SqliteMigrator, migrate

from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel


def execute_migrate():
    """
    版本升级 1.2.13 => 1.3.1
    :return:
    """
    migrator = SqliteMigrator(db)

    migrate(
        migrator.add_column(DomainModel._meta.table_name, DomainModel.port.name, DomainModel.port),
        migrator.add_column(DomainModel._meta.table_name, DomainModel.domain_expire_monitor.name, DomainModel.domain_expire_monitor),
    )
