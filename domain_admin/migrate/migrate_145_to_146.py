# -*- coding: utf-8 -*-
"""
@File    : migrate_145_to_146.py
@Date    : 2023-06-14

cmd:
$ python domain_admin/migrate/migrate_136_to_140.py
"""

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
    版本升级 1.4.5 => 1.4.6
    :return:
    """

    migrator = migrate_common.get_migrator(db)

    migrate(
        # add field
        migrator.add_column(NotifyModel._meta.table_name, NotifyModel.comment.name, NotifyModel.comment),
    )
