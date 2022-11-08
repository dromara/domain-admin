# -*- coding: utf-8 -*-
"""
@File    : cert_common.py
@Date    : 2022-11-08
@Author  : Peng Shiyu
"""
import socket

from dateutil import parser

from domain_admin.utils.cert_util import cert_consts


def parse_time(time_str):
    """
    解析并格式化时间
    :param time_str: str
    :return: str
    """
    return parser.parse(time_str).astimezone().strftime(cert_consts.DATETIME_FORMAT)


def parse_domain_with_port(domain_with_port):
    """
    解析域名，允许携带端口号
    :param domain_with_port: str
        例如：
        www.domain.com
        www.domain.com:8888
    :return: dict
    """
    if ':' in domain_with_port:
        domain, port = domain_with_port.split(':')
    else:
        domain = domain_with_port
        port = cert_consts.SSL_DEFAULT_PORT

    if not isinstance(port, int):
        port = int(port)

    return {
        'domain': domain,
        'port': port,
    }


def short_name_convert(data):
    """
    名字转换
    :param data: dict
    :return: dict
    """
    name_map = {
        'C': 'countryName',
        'CN': 'commonName',
        'O': 'organizationName',
        'OU': 'organizationalUnitName',
        'L': 'localityName',
        'ST': 'stateOrProvinceName'
    }

    dct = {}
    for key, value in name_map.items():
        dct[key] = data.get(value, '')

    return dct


def get_domain_ip(domain):
    """
    获取ip地址
    :param domain: str
    :return: str
    """
    return socket.gethostbyname(domain)
