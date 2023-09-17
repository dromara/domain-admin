# -*- coding: utf-8 -*-
"""
@File    : migrate_1523_to_1524.py
@Date    : 2023-09-17

cmd:
$ python domain_admin/migrate/migrate_1523_to_1524.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel


def execute_migrate():
    """
    版本升级 1.5.23 => 1.5.24
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        migrator.add_column(
            DomainModel._meta.table_name,
            DomainModel.ssl_type.name,
            DomainModel.ssl_type
        ),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
