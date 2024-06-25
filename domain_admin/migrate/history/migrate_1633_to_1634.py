# -*- coding: utf-8 -*-
"""
@File    : migrate_1633_to_1634.py
@Date    : 2024-06-24

cmd:
$ python domain_admin/migrate/migrate_1633_to_1634.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.issue_certificate_model import IssueCertificateModel, DeployStatusEnum


def execute_migrate():
    """
    版本升级 1.6.33 => 1.6.34
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # challenge_deploy_type_id
        migrator.add_column(
            table=IssueCertificateModel._meta.table_name,
            column_name=IssueCertificateModel.challenge_deploy_type_id.name,
            field=IssueCertificateModel.challenge_deploy_type_id
        ),

        # challenge_deploy_id
        migrator.add_column(
            table=IssueCertificateModel._meta.table_name,
            column_name=IssueCertificateModel.challenge_deploy_id.name,
            field=IssueCertificateModel.challenge_deploy_id
        ),

        # challenge_deploy_status
        migrator.add_column(
            table=IssueCertificateModel._meta.table_name,
            column_name=IssueCertificateModel.challenge_deploy_status.name,
            field=IssueCertificateModel.challenge_deploy_status
        ),

        # deploy_type_id
        migrator.add_column(
            table=IssueCertificateModel._meta.table_name,
            column_name=IssueCertificateModel.deploy_type_id.name,
            field=IssueCertificateModel.deploy_type_id
        ),

        # deploy_url
        migrator.add_column(
            table=IssueCertificateModel._meta.table_name,
            column_name=IssueCertificateModel.deploy_url.name,
            field=IssueCertificateModel.deploy_url
        ),

        # deploy_header_raw
        migrator.add_column(
            table=IssueCertificateModel._meta.table_name,
            column_name=IssueCertificateModel.deploy_header_raw.name,
            field=IssueCertificateModel.deploy_header_raw
        ),

        # ssl_deploy_status
        migrator.add_column(
            table=IssueCertificateModel._meta.table_name,
            column_name=IssueCertificateModel.ssl_deploy_status.name,
            field=IssueCertificateModel.ssl_deploy_status
        ),

        # version
        migrator.add_column(
            table=IssueCertificateModel._meta.table_name,
            column_name=IssueCertificateModel.version.name,
            field=IssueCertificateModel.version
        ),

    ]

    migrate_common.try_execute_migrate(migrate_rows)

    # update data
    rows = IssueCertificateModel.select().where(
        IssueCertificateModel.is_auto_renew == True
    )

    for row in rows:
        IssueCertificateModel.update(
            challenge_deploy_id=row.deploy_host_id,
            challenge_deploy_status=DeployStatusEnum.SUCCESS,
            ssl_deploy_status=DeployStatusEnum.SUCCESS
        ).where(
            IssueCertificateModel.id == row.id
        ).execute()
