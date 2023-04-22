# -*- coding: utf-8 -*-
"""
@File    : migrate_110_to_1212.py
@Date    : 2023-02-06

cmd:
$ python domain_admin/migrate/migrate_110_to_1212.py
"""

from playhouse.migrate import SqliteMigrator, migrate

from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel


def execute_migrate():
    """
    版本升级 1.1.0 => 1.2.12
    :return:
    """
    migrator = SqliteMigrator(db)

    migrate(
        migrator.add_column(DomainModel._meta.table_name, DomainModel.domain_check_time.name, DomainModel.domain_check_time),
        migrator.add_column(DomainModel._meta.table_name, DomainModel.ip_check_time.name, DomainModel.ip_check_time),
    )
