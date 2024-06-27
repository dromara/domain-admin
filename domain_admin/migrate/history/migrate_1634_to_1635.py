# -*- coding: utf-8 -*-
"""
@File    : migrate_1634_to_1635.py
@Date    : 2024-06-24

cmd:
$ python domain_admin/migrate/migrate_1634_to_1635.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.issue_certificate_model import IssueCertificateModel, DeployStatusEnum


def execute_migrate():
    """
    版本升级 1.6.34 => 1.6.35
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # directory_type
        migrator.add_column(
            table=IssueCertificateModel._meta.table_name,
            column_name=IssueCertificateModel.directory_type.name,
            field=IssueCertificateModel.directory_type
        ),

        # key_type
        migrator.add_column(
            table=IssueCertificateModel._meta.table_name,
            column_name=IssueCertificateModel.key_type.name,
            field=IssueCertificateModel.key_type
        ),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
