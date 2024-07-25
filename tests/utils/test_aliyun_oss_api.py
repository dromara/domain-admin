# -*- coding: utf-8 -*-
"""
@File    : test_aliyun_oss_api.py
@Date    : 2024-07-25
"""
import unittest

from domain_admin.utils.open_api import aliyun_oss_api


class AliyunOSSApiTest(unittest.TestCase):

    def test_cname_to_oss_info(self):
        domain = 'cdn.baidu.com'
        oss_info = aliyun_oss_api.cname_to_oss_info(domain)
        print(oss_info)