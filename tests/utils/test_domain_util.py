# -*- coding: utf-8 -*-
"""
@File    : cert_util_test.py
@Date    : 2022-10-22
@Author  : Peng Shiyu
"""
import os

from domain_admin.utils import domain_util


def test_parse_domain():
    filename = '../../docs/domain.txt'

    if os.path.exists(filename):
        lst = domain_util.parse_domain_from_file(filename)
        for line in lst:
            print(line)


def test_extract_domain():
    filename = '../../docs/domain.txt'

    if os.path.exists(filename):
        lst = domain_util.parse_domain_from_file(filename)
        for line in lst:
            print(domain_util.extract_domain(line))


def test_parse_domain_from_txt_file():
    """
    测试域名解析函数
    :return:
    """
    domain_filename = '../../docs/domain.txt'
    domain_expect_filename = '../../docs/domain-expect.txt'

    expect_domains = None
    with open(domain_expect_filename, 'r') as f:
        expect_domains = [row.strip() for row in f.readlines()]

    if os.path.exists(domain_filename):
        lst = domain_util.parse_domain_from_txt_file(domain_filename)
        for index, row in enumerate(lst):
            assert row['domain'] == expect_domains[index]
