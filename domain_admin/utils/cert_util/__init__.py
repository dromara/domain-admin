# -*- coding: utf-8 -*-
"""
@File    : __init__.py.py
@Date    : 2022-11-08
@Author  : Peng Shiyu
"""

from .cert_socket import get_cert_info as get_cert_info_by_socket
from .cert_openssl import get_cert_info as get_cert_info_by_openssl


def get_cert_info(domain_with_port):
    """
    工厂方法
    :param domain_with_port:
    :return:
    """
    cert_info = None

    try:
        cert_info = get_cert_info_by_socket(domain_with_port)
    except:
        pass

    if not cert_info:
        cert_info = get_cert_info_by_openssl(domain_with_port)

    return cert_info
