# -*- coding: utf-8 -*-
"""
@File    : cert_util_test.py
@Date    : 2022-10-22
@Author  : Peng Shiyu
"""

from domain_admin.utils import domain_util


def test_parse_domain():
    for line in domain_util.parse_domain_from_file('../../doc/domain.txt'):
        print(line)
