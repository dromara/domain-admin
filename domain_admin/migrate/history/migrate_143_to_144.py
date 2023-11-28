# -*- coding: utf-8 -*-
"""
@File    : migrate_143_to_144.py
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
from domain_admin.model.system_model import SystemModel
from domain_admin.model.user_model import UserModel


def execute_migrate():
    """
    版本升级 1.4.3 => 1.4.4
    :return:
    """

    migrator = migrate_common.get_migrator(db)

    # remove row
    SystemModel.delete().where(
        SystemModel.key == 'mail_subject'
    ).execute()

    migrate_rows = [
        #  remove column
        migrator.drop_column(UserModel._meta.table_name, 'before_expire_days'),
        migrator.drop_column(UserModel._meta.table_name, 'email_list_raw'),

        # add field
        migrator.add_column(NotifyModel._meta.table_name, NotifyModel.expire_days.name, NotifyModel.expire_days),

        # remove index NotifyModel
        migrator.drop_index(NotifyModel._meta.table_name, 'notifymodel_user_id_type_id'),
    ]

    migrate_common.try_execute_migrate(migrate_rows)
