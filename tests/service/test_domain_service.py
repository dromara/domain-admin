# -*- coding: utf-8 -*-
"""
@File    : test_domain_service.py
@Date    : 2023-06-03
"""
from domain_admin.model.domain_model import DomainModel
from domain_admin.service import domain_service


def test_update_domain_row():
    row = DomainModel.get_by_id(1)
    domain_service.update_domain_row(row)
