# -*- coding: utf-8 -*-

from .base_model import db
from .domain_model import DomainModel

tables = [
    DomainModel,
]

for table in tables:
    if not table.table_exists():
        table.create_table()
