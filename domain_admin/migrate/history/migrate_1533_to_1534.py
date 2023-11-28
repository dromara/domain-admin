# -*- coding: utf-8 -*-
"""
@File    : migrate_1533_to_1534.py
@Date    : 2023-09-17

cmd:
$ python domain_admin/migrate/migrate_1533_to_1534.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.notify_model import NotifyModel


def execute_migrate():
    """
    版本升级 1.5.33 => 1.5.34
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        migrator.add_column(
            NotifyModel._meta.table_name,
            NotifyModel.groups_raw.name,
            NotifyModel.groups_raw
        ),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
