# -*- coding: utf-8 -*-
"""
@File    : cert_util_v2.py
@Date    : 2022-10-22
@Author  : Peng Shiyu

通过socket 获取域名ssl 证书信息

参考：
Python脚本批量检查SSL证书过期时间
https://linuxeye.com/479.html
"""

import json
import socket
import ssl

from dateutil import parser

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

socket.setdefaulttimeout(5)


def get_domain_ip(domain):
    """
    获取ip地址
    :param domain: str
    :return: str
    """
    return socket.gethostbyname(domain)


def get_domain_cert(domain):
    """
    获取证书信息
    :param domain: str
    :return: dict
    """
    cxt = ssl.create_default_context()
    wrap_socket = cxt.wrap_socket(socket.socket(), server_hostname=domain)

    wrap_socket.connect((domain, 443))
    cert = wrap_socket.getpeercert()
    wrap_socket.close()

    return cert


def get_cert_info(domain):
    """
    获取证书信息
    :param domain: str
    :return: dict
    """
    cert = get_domain_cert(domain)

    issuer = _tuple_to_dict(cert['issuer'])
    subject = _tuple_to_dict(cert['subject'])

    return {
        'domain': domain,
        'ip': get_domain_ip(domain),
        'subject': _name_convert(subject),
        'issuer': _name_convert(issuer),
        # 'version': cert['version'],
        # 'serial_number': cert['serialNumber'],
        'start_date': _parse_time(cert['notBefore']),
        'expire_date': _parse_time(cert['notAfter']),
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


def _name_convert(data):
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


def _parse_time(time_str):
    """
    解析并格式化时间
    :param time_str: str
    :return: str
    """
    return parser.parse(time_str).astimezone().strftime(DATETIME_FORMAT)


if __name__ == "__main__":
    print(json.dumps(get_cert_info("www.baidu.com"), ensure_ascii=False, indent=2))
