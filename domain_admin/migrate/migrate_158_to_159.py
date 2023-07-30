# -*- coding: utf-8 -*-
"""
@File    : migrate_158_to_159.py
@Date    : 2023-06-30

cmd:
$ python domain_admin/migrate/migrate_158_to_159.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.issue_certificate_model import IssueCertificateModel
from domain_admin.model.user_model import UserModel


def execute_migrate():
    """
    版本升级 1.5.8 => 1.5.9
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # add column
        migrator.add_column(
            IssueCertificateModel._meta.table_name,
            IssueCertificateModel.challenge_type.name,
            IssueCertificateModel.challenge_type),

        # add column
        migrator.add_column(
            IssueCertificateModel._meta.table_name,
            IssueCertificateModel.deploy_host_id.name,
            IssueCertificateModel.deploy_host_id
        ),

        migrator.add_column(
            IssueCertificateModel._meta.table_name,
            IssueCertificateModel.deploy_verify_path.name,
            IssueCertificateModel.deploy_verify_path
        ),

        migrator.add_column(
            IssueCertificateModel._meta.table_name,
            IssueCertificateModel.deploy_key_file.name,
            IssueCertificateModel.deploy_key_file
        ),

        migrator.add_column(
            IssueCertificateModel._meta.table_name,
            IssueCertificateModel.deploy_fullchain_file.name,
            IssueCertificateModel.deploy_fullchain_file
        ),

        migrator.add_column(
            IssueCertificateModel._meta.table_name,
            IssueCertificateModel.deploy_reloadcmd.name,
            IssueCertificateModel.deploy_reloadcmd
        ),

        migrator.add_column(
            IssueCertificateModel._meta.table_name,
            IssueCertificateModel.is_auto_renew.name,
            IssueCertificateModel.is_auto_renew
        ),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
