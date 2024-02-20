# -*- coding: utf-8 -*-
"""
@File    : migrate_168_to_169.py
@Date    : 2023-09-17

cmd:
$ python domain_admin/migrate/migrate_168_to_169.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.address_model import AddressModel
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.notify_model import NotifyModel


def execute_migrate():
    """
    版本升级 1.6.8 => 1.6.9
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        migrator.add_column(
            table=AddressModel._meta.table_name,
            column_name=AddressModel.source.name,
            field=AddressModel.source
        ),

        migrator.add_column(
            table=AddressModel._meta.table_name,
            column_name=AddressModel.comment.name,
            field=AddressModel.comment
        ),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
