# -*- coding: utf-8 -*-
"""
@File    : cert_common.py
@Date    : 2022-11-08
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import socket

import OpenSSL
from dateutil import parser

from domain_admin.utils import time_util
from domain_admin.utils.cert_util import cert_consts


def parse_time(time_str):
    """
    解析并格式化时间
    :param time_str: str
    :return: str
    """
    return parser.parse(time_str).astimezone().strftime(cert_consts.DATETIME_FORMAT)


def parse_datetime(time_str):
    """
    解析时间
    :param time_str: str
    :return: datetime
    """
    return parser.parse(time_str).astimezone().replace(tzinfo=None)


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


class X509Item(object):
    version = ''
    subject = dict()
    issuer = dict()
    notAfter = ''
    notBefore = ''
    serialNumber = ''
    signatureAlgorithm = ''
    hasExpired = None
    subjectAltName = []

    def to_dict(self):
        return {
            'subject': self.subject,
            'version': self.version,
            'issuer': self.issuer,
            'notAfter': self.notAfter,
            'notBefore': self.notBefore,
            'serialNumber': self.serialNumber,
            'signatureAlgorithm': self.signatureAlgorithm,
            'subjectAltName': self.subjectAltName,
            'hasExpired': self.hasExpired,
            'expireDays': self.expireDays,
        }

    @property
    def expireDays(self):
        return time_util.get_diff_days(self.notBefore, self.notAfter)


def dump_certificate_to_text(ssl_cert):
    """
    将证书对象转为字符串text形式
    :param ssl_cert:
    :return: str
    """
    return OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_TEXT, ssl_cert).decode('utf-8')


def dump_certificate_to_pem(ssl_cert):
    """
    将证书对象转为字符串pem形式
    :param ssl_cert:
    :return: str
    """
    return OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, ssl_cert).decode('utf-8')


def parse_cert(ssl_cert):
    """
    解析证书
    :param ssl_cert:
    :return:
    """
    item = X509Item()

    issuer = {}
    for [name, value] in ssl_cert.get_issuer().get_components():
        issuer[name.decode()] = value.decode()

    item.issuer = issuer

    subject = {}
    for [name, value] in ssl_cert.get_subject().get_components():
        subject[name.decode()] = value.decode()

    item.subject = subject

    item.version = ssl_cert.get_version()
    item.hasExpired = ssl_cert.has_expired()
    item.notAfter = time_util.parse_time(ssl_cert.get_notAfter().decode())
    item.notBefore = time_util.parse_time(ssl_cert.get_notBefore().decode())
    # ref: https://stackoverflow.com/questions/39286805/x-509-certificate-serial-number-to-hex-conversion
    item.serialNumber = '{0:x}'.format(ssl_cert.get_serial_number()).upper()
    item.signatureAlgorithm = ssl_cert.get_signature_algorithm().decode()

    item.subjectAltName = get_certificate_san(ssl_cert)

    return item


def get_certificate_san(x509cert):
    """
    获取SAN域名列表
    ref: https://cloud.tencent.com/developer/ask/sof/141600
    :param x509cert:
    :return:
    """
    dns_names = []

    ext_count = x509cert.get_extension_count()

    for i in range(0, ext_count):
        ext = x509cert.get_extension(i)
        if 'subjectAltName' in str(ext.get_short_name()):
            for item in str(ext).split(', '):

                if item.startswith('DNS:'):
                    key, value = item.split(':')
                    dns_names.append(value.strip())

    return dns_names
