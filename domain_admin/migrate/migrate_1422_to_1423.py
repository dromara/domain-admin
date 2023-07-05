# -*- coding: utf-8 -*-
"""
@File    : migrate_1422_to_1423.py
@Date    : 2023-06-30

cmd:
$ python domain_admin/migrate/migrate_1413_to_1414.py
"""

from playhouse.migrate import SqliteMigrator, migrate

from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.notify_model import NotifyModel


def execute_migrate():
    """
    版本升级 1.4.22 => 1.4.23
    :return:
    """
    migrator = migrate_common.get_migrator(db)

    migrate(
        # remove index NotifyModel again
        migrator.drop_index(NotifyModel._meta.table_name, 'notifymodel_user_id_type_id'),
    )
