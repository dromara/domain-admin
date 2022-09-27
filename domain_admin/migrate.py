# -*- coding: utf-8 -*-
from playhouse.migrate import SqliteMigrator, migrate

from domain_admin.model import db, DomainModel

if __name__ == '__main__':
    migrator = SqliteMigrator(db)

    migrate(
        # 2022-09-27
        # migrator.add_column(DomainModel._meta.table_name, DomainModel.notify_status.name, DomainModel.notify_status),
        # migrator.add_column(DomainModel._meta.table_name, DomainModel.ip.name, DomainModel.ip),
    )
