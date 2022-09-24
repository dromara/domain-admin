# -*- coding: utf-8 -*-
from .group_model import GroupModel
from .base_model import db
from .domain_model import DomainModel

tables = [
    DomainModel,
    GroupModel,
]

for table in tables:
    if not table.table_exists():
        table.create_table()
