# -*- coding: utf-8 -*-
"""
@File    : migrate_140_alpha_to_140.py
@Date    : 2023-06-14

cmd:
$ python domain_admin/migrate/migrate_136_to_140.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from playhouse.migrate import migrate

from domain_admin.migrate import migrate_common
from domain_admin.model.address_model import AddressModel
from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.notify_model import NotifyModel


def execute_migrate():
    """
    版本升级 1.4.0-alpha => 1.4.0
    :return:
    """

    migrator = migrate_common.get_migrator(db)

    migrate_rows = [
        # add NotifyModel field
        migrator.add_column(NotifyModel._meta.table_name, NotifyModel.status.name, NotifyModel.status),
        migrator.add_column(NotifyModel._meta.table_name, NotifyModel.event_id.name, NotifyModel.event_id),

        # remove AddressModel field
        migrator.drop_column(AddressModel._meta.table_name, 'host_connect_status'),
        migrator.drop_column(AddressModel._meta.table_name, 'host_check_time'),
        migrator.drop_column(AddressModel._meta.table_name, 'host_status_monitor'),
        migrator.drop_column(AddressModel._meta.table_name, 'ssl_check_time'),
        migrator.drop_column(AddressModel._meta.table_name, 'ssl_auto_update'),
        migrator.drop_column(AddressModel._meta.table_name, 'ssl_expire_monitor'),

        # remove DomainModel field
        migrator.drop_column(DomainModel._meta.table_name, 'notify_status'),
        migrator.drop_column(DomainModel._meta.table_name, 'detail_raw'),
        migrator.drop_column(DomainModel._meta.table_name, 'ip'),
        migrator.drop_column(DomainModel._meta.table_name, 'ip_check_time'),
        migrator.drop_column(DomainModel._meta.table_name, 'ip_auto_update'),
        migrator.drop_column(DomainModel._meta.table_name, 'check_time'),
        migrator.drop_column(DomainModel._meta.table_name, 'domain_start_time'),
        migrator.drop_column(DomainModel._meta.table_name, 'domain_expire_time'),
        migrator.drop_column(DomainModel._meta.table_name, 'domain_expire_days'),
        migrator.drop_column(DomainModel._meta.table_name, 'domain_check_time'),
        migrator.drop_column(DomainModel._meta.table_name, 'domain_auto_update'),
        migrator.drop_column(DomainModel._meta.table_name, 'domain_expire_monitor'),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
