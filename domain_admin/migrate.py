# -*- coding: utf-8 -*-
from playhouse.migrate import SqliteMigrator, migrate

from domain_admin.model.base_model import db
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel

if __name__ == '__main__':
    migrator = SqliteMigrator(db)

    migrate(
        # 2022-09-28
        # migrator.add_column(DomainModel._meta.table_name, DomainModel.user_id.name, DomainModel.user_id),
        # migrator.add_column(GroupModel._meta.table_name, GroupModel.user_id.name, GroupModel.user_id),

        # 2022-09-27
        # migrator.add_column(DomainModel._meta.table_name, DomainModel.notify_status.name, DomainModel.notify_status),
        # migrator.add_column(DomainModel._meta.table_name, DomainModel.ip.name, DomainModel.ip),
    )
