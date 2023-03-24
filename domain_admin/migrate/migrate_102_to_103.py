# -*- coding: utf-8 -*-
"""
@File    : migrate_102_to_103.py
@Date    : 2023-02-06

cmd:
$ python domain_admin/migrate/migrate_102_to_103.py
"""

from playhouse.migrate import SqliteMigrator, migrate

from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel


def execute_migrate():
    """
    版本升级 1.0.2 => 1.0.3
    :return:
    """
    migrator = SqliteMigrator(db)

    migrate(
        migrator.add_column(DomainModel._meta.table_name, DomainModel.is_monitor.name, DomainModel.is_monitor),
    )
