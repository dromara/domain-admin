# -*- coding: utf-8 -*-
"""
@File    : migrate_1670_to_1671.py
@Date    : 2025-08-17

cmd:
$ python domain_admin/migrate/migrate_1670_to_1671.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.log_async_task_model import AsyncTaskModel
from domain_admin.model.monitor_model import MonitorModel


def execute_migrate():
    """
    版本升级 v1.6.70 => v1.6.71
    :return:
    """

    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        migrator.add_column(
            table=AsyncTaskModel._meta.table_name,
            column_name=AsyncTaskModel.params.name,
            field=AsyncTaskModel.params
        )
    ]

    migrate_common.try_execute_migrate(migrate_rows)
