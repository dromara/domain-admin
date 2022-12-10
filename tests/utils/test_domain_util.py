# -*- coding: utf-8 -*-
"""
@File    : cert_util_test.py
@Date    : 2022-10-22
@Author  : Peng Shiyu
"""
import os

from domain_admin.utils import domain_util


def test_parse_domain():
    filename = '../../doc/domain.txt'

    if os.path.exists(filename):
        lst = domain_util.parse_domain_from_file('../../doc/domain.txt')
        for line in lst:
            print(line)
