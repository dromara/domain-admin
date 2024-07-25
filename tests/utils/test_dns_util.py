# -*- coding: utf-8 -*-
"""
@File    : dns_util_test.py
@Date    : 2022-10-22
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import socket
import unittest

from domain_admin.enums.ssl_type_enum import SSLTypeEnum
from domain_admin.utils import cert_util, dns_util
from domain_admin.utils.cert_util import cert_socket_v2, cert_openssl_v2


class DnsUtilTest(unittest.TestCase):

    def test_query_domain_cname(self):
        print(dns_util.query_domain_cname('test.tiedankyy.com'))
