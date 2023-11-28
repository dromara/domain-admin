# -*- coding: utf-8 -*-
"""
@File    : migrate_102_to_103.py
@Date    : 2023-02-06

cmd:
$ python domain_admin/migrate/migrate_102_to_103.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel


def execute_migrate():
    """
    版本升级 1.0.6 => 1.1.0
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        migrator.add_column(
            DomainModel._meta.table_name,
            DomainModel.domain_start_time.name,
            DomainModel.domain_start_time),

        migrator.add_column(
            DomainModel._meta.table_name,
            DomainModel.domain_expire_time.name,
            DomainModel.domain_expire_time),

        migrator.add_column(
            DomainModel._meta.table_name,
            DomainModel.domain_expire_days.name,
            DomainModel.domain_expire_days),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
