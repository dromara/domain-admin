# -*- coding: utf-8 -*-
"""
@File    : migrate_136_to_140_alpha.py
@Date    : 2023-06-14

cmd:
$ python domain_admin/migrate/migrate_136_to_140.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from playhouse.migrate import migrate

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel


def execute_migrate():
    """
    版本升级 1.3.6 => 1.4.0-alpha
    :return:
    """

    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        migrator.add_column(
            DomainModel._meta.table_name,
            DomainModel.root_domain.name,
            DomainModel.root_domain),

        migrator.add_column(
            DomainModel._meta.table_name,
            DomainModel.is_dynamic_host.name,
            DomainModel.is_dynamic_host),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
