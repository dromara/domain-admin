# -*- coding: utf-8 -*-
"""
@File    : cert_service_test.py
@Date    : 2024-08-05
"""
import unittest

from domain_admin.service import cert_service
from domain_admin.utils import json_util
from domain_admin.utils.cert_util import cert_common, cert_openssl_v2


class CertServiceTest(unittest.TestCase):
    def test_get_cert_information(self):
        domain = 'https://www.boc.cn/'
        ret = cert_service.get_cert_information(domain=domain)
        print(json_util.json_dump(ret))

    def test_is_extended_validation(self):
        cert = cert_openssl_v2.get_ssl_cert('www.boc.cn')
        # ret = cert_common.is_extended_validation(cert)
        # print(ret)