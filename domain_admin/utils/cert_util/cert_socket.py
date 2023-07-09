# -*- coding: utf-8 -*-
"""
@File    : cert_socket.py
@Date    : 2022-10-22
@Author  : Peng Shiyu

通过socket 获取域名ssl 证书信息

参考：
Python脚本批量检查SSL证书过期时间
https://linuxeye.com/479.html
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import socket
import ssl
import warnings
from domain_admin.utils.cert_util import cert_consts, cert_common


# warnings.warn("cert_socket.py is Deprecated, please use cert_socket_v2.py")


def create_ssl_context():
    """
    ssl上下文
    :return:
    """

    return ssl.create_default_context()


def get_domain_cert(host, port=443, timeout=3):
    """
    获取证书信息
    存在问题：没有指定主机ip，不一定能获取到正确的证书信息
    :param host: str
    :param port: int
    :param timeout: int
    :return: dict
    """
    context = ssl.create_default_context()

    with socket.create_connection(address=(host, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=host) as wrap_socket:
            return wrap_socket.getpeercert()


def get_cert_info(domain_with_port):
    """
    获取证书信息
    :param domain_with_port: str
    :return: dict
    """
    domain_info = cert_common.parse_domain_with_port(domain_with_port)
    domain = domain_info.get('domain')
    port = domain_info.get('port', cert_consts.SSL_DEFAULT_PORT)

    cert = get_domain_cert(domain, port)

    issuer = _tuple_to_dict(cert['issuer'])
    subject = _tuple_to_dict(cert['subject'])

    return {
        'domain': domain_with_port,
        # 'ip': cert_common.get_domain_ip(domain),
        'subject': cert_common.short_name_convert(subject),
        'issuer': cert_common.short_name_convert(issuer),
        # 'version': cert['version'],
        # 'serial_number': cert['serialNumber'],
        'start_date': cert_common.parse_time(cert['notBefore']),
        'expire_date': cert_common.parse_time(cert['notAfter']),
    }


def _tuple_to_dict(cert_tuple):
    """
    cert证书 tuple转dict
    :param cert_tuple: tuple
    :return:
    """
    data = {}
    for item in cert_tuple:
        data[item[0][0]] = item[0][1]

    return data


if __name__ == '__main__':
    print(get_cert_info('www.baidu.com'))
    # not support
    # print(get_cert_info('www.mysite.com'))
