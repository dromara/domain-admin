# -*- coding: utf-8 -*-
"""
@File    : migrate_151_to_152.py
@Date    : 2023-06-30

cmd:
$ python domain_admin/migrate/migrate_151_to_152.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.notify_model import NotifyModel


def execute_migrate():
    """
    版本升级 1.5.1 => 1.5.2
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # add icp_company
        migrator.add_column(
            DomainInfoModel._meta.table_name,
            DomainInfoModel.icp_company.name,
            DomainInfoModel.icp_company),
        # add icp_licence
        migrator.add_column(
            DomainInfoModel._meta.table_name,
            DomainInfoModel.icp_licence.name,
            DomainInfoModel.icp_licence),
        # add 标签list
        migrator.add_column(
            DomainInfoModel._meta.table_name,
            DomainInfoModel.tags_raw.name,
            DomainInfoModel.tags_raw),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
