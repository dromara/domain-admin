# -*- coding: utf-8 -*-
"""
@File    : migrate_1625_to_1626.py
@Date    : 2024-02-24

cmd:
$ python domain_admin/migrate/migrate_1625_to_1626.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.address_model import AddressModel
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.host_model import HostModel
from domain_admin.model.monitor_model import MonitorModel
from domain_admin.model.notify_model import NotifyModel


def execute_migrate():
    """
    版本升级 1.6.25 => 1.6.26
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # version
        migrator.alter_column_type(
            table=HostModel._meta.table_name,
            column=HostModel.private_key,
            field=HostModel.private_key
        )
    ]

    migrate_common.try_execute_migrate(migrate_rows)
