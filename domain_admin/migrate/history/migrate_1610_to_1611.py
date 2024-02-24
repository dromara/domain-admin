# -*- coding: utf-8 -*-
"""
@File    : migrate_1610_to_1611.py
@Date    : 2024-02-24

cmd:
$ python domain_admin/migrate/migrate_1610_to_1611.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.address_model import AddressModel
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.monitor_model import MonitorModel
from domain_admin.model.notify_model import NotifyModel


def execute_migrate():
    """
    版本升级 1.6.10 => 1.6.11
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # version
        migrator.add_column(
            table=MonitorModel._meta.table_name,
            column_name=MonitorModel.version.name,
            field=MonitorModel.version
        )
    ]

    migrate_common.try_execute_migrate(migrate_rows)
