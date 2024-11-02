# -*- coding: utf-8 -*-
"""
@File    : migrate_1655_to_1656.py
@Date    : 2024-08-28

cmd:
$ python domain_admin/migrate/migrate_1655_to_1656.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.monitor_model import MonitorModel


def execute_migrate():
    """
    版本升级 v1.6.55 => v1.6.56
    :return:
    """

    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        migrator.add_column(
            table=MonitorModel._meta.table_name,
            column_name=MonitorModel.interval_unit.name,
            field=MonitorModel.interval_unit
        )
    ]

    migrate_common.try_execute_migrate(migrate_rows)
