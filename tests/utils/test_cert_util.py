# -*- coding: utf-8 -*-
"""
@File    : cert_util_test.py
@Date    : 2022-10-22
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import socket

from domain_admin.enums.ssl_type_enum import SSLTypeEnum
from domain_admin.utils import cert_util
from domain_admin.utils.cert_util import cert_socket_v2, cert_openssl_v2


def test_get_cert_info():
    # print(cert_util.get_cert_info('dfyun-spare1.showdoc.com.cn:8888'))
    print(cert_util.get_cert_info('www.baidu.com'))


def test_cert_socket_v2():
    ret = cert_socket_v2.get_ssl_cert_info(
        # 'www.csdn.net',
        # '123.129.227.79',
        # '38.60.47.102',
        # '38.60.47.102'
        'juejin.cn', '223.111.193.232'
    )
    print(ret)


def test_get_domain_host_list():
    ret = cert_socket_v2.get_domain_host_list('report.tibcn.cn', 443)
    print(ret)


def test_getaddrinfo():
    # ret = socket.getaddrinfo('report.tibcn.cn', 443, proto=socket.IPPROTO_TCP)
    ret = socket.getaddrinfo('www.baidu.com', 443, proto=socket.IPPROTO_TCP)
    for item in ret:
        print(item)


def test_get_default_verify_paths():
    import ssl
    print(ssl.get_default_verify_paths())


def test_get_ssl_cert_by_openssl():
    lst = [
        ('cdn-image-01.kaishuleyuan.com', '101.96.145.100'),
        ('www.tmall.com', '27.128.222.198'),
        ('juejin.cn', '150.138.144.89'),
        ('dev.csdn.net', '120.46.209.149'),
        ('38.60.47.102', '38.60.47.102'),
        ('pgmanage.qnvip.com', '121.196.205.251'),
    ]

    for domain, host in lst:
        print(cert_openssl_v2.get_ssl_cert_by_openssl(domain, host, 443))


def test_get_smtp_cert_by_openssl():
    lst = [

        ('mail.drees-email.de', '2.59.135.189', 25),
        # ('mail.drees-email.de', '2.59.135.189', 587),
        # ('mail.drees-email.de', '2.59.135.189', 465),
        # ('smtp.163.com', '123.126.97.113', 465),
        # ('smtp.163.com', '123.126.97.113', 587),
        # ('smtp.163.com', '123.126.97.113', 25),
    ]

    for domain, host, port in lst:
        print(cert_openssl_v2.get_ssl_cert_by_openssl(domain, host, port, ssl_type=SSLTypeEnum.START_TLS))
