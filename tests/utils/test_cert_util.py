# -*- coding: utf-8 -*-
"""
@File    : cert_util_test.py
@Date    : 2022-10-22
@Author  : Peng Shiyu
"""

from domain_admin.utils import cert_util


def test_get_cert_info():
    # print(cert_util.get_cert_info('dfyun-spare1.showdoc.com.cn:8888'))
    print(cert_util.get_cert_info('www.baidu.com'))
