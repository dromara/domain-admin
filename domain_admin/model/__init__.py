# -*- coding: utf-8 -*-
from domain_admin.model.user_model import UserModel
from .group_model import GroupModel
from .base_model import db
from .domain_model import DomainModel

tables = [
    DomainModel,
    GroupModel,
    UserModel,
]

for table in tables:
    if not table.table_exists():
        table.create_table()
