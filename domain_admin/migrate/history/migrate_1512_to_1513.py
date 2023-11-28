# -*- coding: utf-8 -*-
"""
@File    : migrate_1512_to_1513.py
@Date    : 2023-08-03

cmd:
$ python domain_admin/migrate/migrate_1512_to_1513.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.host_model import HostModel


def execute_migrate():
    """
    版本升级 1.5.12 => 1.5.13
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # add column
        migrator.add_column(
            HostModel._meta.table_name,
            HostModel.auth_type.name,
            HostModel.auth_type
        ),

        # add column
        migrator.add_column(
            HostModel._meta.table_name,
            HostModel.private_key.name,
            HostModel.private_key
        ),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
