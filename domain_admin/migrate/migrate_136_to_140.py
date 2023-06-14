# -*- coding: utf-8 -*-
"""
@File    : migrate_136_to_140.py
@Date    : 2023-06-14

cmd:
$ python domain_admin/migrate/migrate_136_to_140.py
"""

from playhouse.migrate import SqliteMigrator, migrate, SchemaMigrator

from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel


def execute_migrate():
    """
    版本升级 1.3.6 => 1.4.0
    :return:
    """
    migrator = SchemaMigrator(db)

    migrate(
        migrator.add_column(DomainModel._meta.table_name, DomainModel.root_domain.name, DomainModel.root_domain),
    )
