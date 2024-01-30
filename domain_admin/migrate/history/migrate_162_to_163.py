# -*- coding: utf-8 -*-
"""
@File    : migrate_162_to_163.py
@Date    : 2023-09-17

cmd:
$ python domain_admin/migrate/migrate_162_to_163.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.notify_model import NotifyModel


def execute_migrate():
    """
    版本升级 1.6.2 => 1.6.3
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        migrator.add_column(
            DomainInfoModel._meta.table_name,
            DomainInfoModel.version.name,
            DomainInfoModel.version
        ),

        migrator.add_column(
            DomainModel._meta.table_name,
            DomainModel.version.name,
            DomainModel.version
        ),

    ]

    migrate_common.try_execute_migrate(migrate_rows)
