# -*- coding: utf-8 -*-
"""
@File    : migrate_154_to_155.py
@Date    : 2023-06-30

cmd:
$ python domain_admin/migrate/migrate_154_to_155.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.user_model import UserModel


def execute_migrate():
    """
    版本升级 1.5.4 => 1.5.5
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # add role
        migrator.add_column(
            UserModel._meta.table_name,
            UserModel.role.name,
            UserModel.role),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
