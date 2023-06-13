# -*- coding: utf-8 -*-
"""
@File    : cert_util_test.py
@Date    : 2022-10-22
@Author  : Peng Shiyu
"""
import socket

from domain_admin.utils import cert_util
from domain_admin.utils.cert_util import cert_socket_v2


def test_get_cert_info():
    # print(cert_util.get_cert_info('dfyun-spare1.showdoc.com.cn:8888'))
    print(cert_util.get_cert_info('www.baidu.com'))


def test_cert_socket_v2():
    ret = cert_socket_v2.get_ssl_cert_info(
        'www.csdn.net',
        '123.129.227.79'
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
