# -*- coding: utf-8 -*-
"""
@File    : domain_icp_service_test.py
@Date    : 2024-01-31
@Author  : Peng Shiyu
"""
import unittest

from domain_admin.service import domain_icp_service


class DomainIcpServiceTest(unittest.TestCase):
    def test_get_domain_icp(self):
        item = domain_icp_service.get_domain_icp('baidu.com')
        print(item)
