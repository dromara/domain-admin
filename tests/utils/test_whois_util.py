# -*- coding: utf-8 -*-
"""
@File    : cert_util_test.py
@Date    : 2022-10-22
@Author  : Peng Shiyu
"""

from domain_admin.utils import whois_util


def test_get_domain_info():
    domain_list = [
        'www.baidu.cn',
        'www.xiaomi.com',
        'dfyun-spare1.showdoc.com.cn:8888',
    ]
    for domain in domain_list:
        print(whois_util.get_domain_info(domain))
