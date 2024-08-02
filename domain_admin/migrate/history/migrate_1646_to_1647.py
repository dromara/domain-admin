# -*- coding: utf-8 -*-
"""
@File    : migrate_1646_to_1647.py
@Date    : 2024-07-24

cmd:
$ python domain_admin/migrate/migrate_1646_to_1647.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.issue_certificate_model import IssueCertificateModel, DeployStatusEnum
from domain_admin.model.tag_model import TagModel


def execute_migrate():
    """
    版本升级 1.6.46 => 1.6.47
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # user_id
        migrator.add_column(
            table=TagModel._meta.table_name,
            column_name=TagModel.user_id.name,
            field=TagModel.user_id
        )
    ]

    migrate_common.try_execute_migrate(migrate_rows)
