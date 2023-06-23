# -*- coding: utf-8 -*-
"""
@File    : cert_socket_v2.py
@Date    : 2023-06-03

参考：python批量检查通一个集群针对同一个域名解析到不同IP地址证书的有效性
https://blog.csdn.net/reblue520/article/details/106832780
"""

import socket
import ssl
import typing

from domain_admin.log import logger
from domain_admin.utils import time_util


def get_domain_host_list(domain: str, port: int = 80) -> typing.List[str]:
    """
    获取域名映射主机地址列表，一对多关系
    :param domain: 域名
    :param port: 端口
    :return: 主机地址列表
    """
    ret = socket.getaddrinfo(
        host=domain,
        port=port,
        family=socket.AF_INET,  # 限制仅返回IPv4
        proto=socket.IPPROTO_TCP)

    lst = []
    for item in ret:
        lst.append(item[4][0])

    return lst


def get_ssl_cert(domain: str, host: str = None, port: int = 443, timeout: int = 3) -> typing.Dict:
    """
    获取主机证书信息
    :param domain:
    :param host:
    :param port:
    :param timeout:
    :return:
    """
    logger.info({
        'domain': domain,
        'host': host,
        'port': port,
        'timeout': timeout
    })

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host, port))

    ssl_context = ssl.create_default_context()

    with ssl_context.wrap_socket(sock, server_hostname=domain) as wrap_socket:
        return wrap_socket.getpeercert()


def get_ssl_cert_info(domain: str, host: str = None, port: int = 443, timeout: int = 3):
    """
    返回解析好的证书信息数据
    :param domain:
    :param host:
    :param port:
    :param timeout:
    :return:
    """
    cert = get_ssl_cert(domain, host, port, timeout)
    print(cert)

    return resolve_cert(cert)


def resolve_cert(cert: typing.Dict):
    """
    解析证书信息，仅解析重要信息
    :param cert:
    :return:
    """
    data = {
        "start_date": time_util.parse_time(cert['notBefore']),
        "expire_date": time_util.parse_time(cert['notAfter']),
    }

    return data


if __name__ == '__main__':
    # print(get_ssl_cert_info('www.taobao.com', '111.62.93.139'))
    print(get_ssl_cert_info('38.60.47.102', '38.60.47.102'))
    # print('www.baidu.com'.encode('idna')) # b'www.baidu.com'
    # print('www.baidu.com'.encode('punycode')) # b'www.baidu.com-'
