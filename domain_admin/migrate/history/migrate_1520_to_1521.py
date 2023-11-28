# -*- coding: utf-8 -*-
"""
@File    : migrate_1520_to_1521.py
@Date    : 2023-08-30

cmd:
$ python domain_admin/migrate/migrate_1520_to_1521.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel


def execute_migrate():
    """
    版本升级 1.5.20 => 1.5.21
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # drop index
        migrator.drop_index(
            DomainModel._meta.table_name,
            'domainmodel_user_id_domain'
        ),

        # add index
        migrator.add_index(
            table=DomainModel._meta.table_name,
            columns=['user_id', 'domain', 'port'],
            unique=True
        ),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
