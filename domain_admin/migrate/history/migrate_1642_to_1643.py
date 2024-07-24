# -*- coding: utf-8 -*-
"""
@File    : migrate_1642_to_1643.py
@Date    : 2024-07-24

cmd:
$ python domain_admin/migrate/migrate_1642_to_1643.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.issue_certificate_model import IssueCertificateModel, DeployStatusEnum


def execute_migrate():
    """
    版本升级 1.6.42 => 1.6.43
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # deploy_params_raw
        migrator.add_column(
            table=IssueCertificateModel._meta.table_name,
            column_name=IssueCertificateModel.deploy_params_raw.name,
            field=IssueCertificateModel.deploy_params_raw
        )
    ]

    migrate_common.try_execute_migrate(migrate_rows)
