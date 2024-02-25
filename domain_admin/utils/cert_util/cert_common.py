# -*- coding: utf-8 -*-
"""
@File    : cert_common.py
@Date    : 2022-11-08
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import socket
from datetime import datetime

import OpenSSL
from dateutil import parser

from domain_admin.utils import time_util
from domain_admin.utils.cert_util import cert_consts

# 证书品牌
cert_brands = [
    'JoySSL',
    'Sectigo',
    'Positive',
    'CFCA',
    'Certum',
    'GlobalSign',
    'TrustAsia',
    'WoTrus',
    'vTrus',
    'BaiduTrust',
    'DigiCert',
    'Symantec',
    'GeoTrust',
    'Rapid',
    'Entrust',
    'Thawte',
    'Sectigo',
    "Let's Encrypt",
]


# 证书类型
class CertTypeByVerifyWayEnum(object):
    DV = 'DV'
    OV = 'OV'
    EV = 'EV'


# 域名数量
class CertDomainTypeEnum(object):
    # 单域名
    Single = 'single'
    # 多域名
    Multiple = 'multiple'
    # 泛域名
    Wildcard = 'wildcard'
    # 混合域名
    Mixed = 'mixed'


certTypeByDomainCountMap = {
    CertDomainTypeEnum.Single: '单域名',
    CertDomainTypeEnum.Multiple: '多域名',
    CertDomainTypeEnum.Wildcard: '泛域名',
    CertDomainTypeEnum.Mixed: '混合域名',
}

CertTypeByVerifyWayEnumMap = {
    CertTypeByVerifyWayEnum.DV: '域名型',
    CertTypeByVerifyWayEnum.OV: '企业型',
    CertTypeByVerifyWayEnum.EV: '增强型',
}


def get_cert_type_by_domain_count(cert):
    """
    获取证书域名数量类型
    :param cert:
    :return:
    """
    # 单个
    if len(cert.subjectAltName) == 1:
        domain = cert.subjectAltName[0]
        if '*' in domain:
            return CertDomainTypeEnum.Wildcard
        else:
            return CertDomainTypeEnum.Single

    # 多个
    for domain in cert.subjectAltName:
        if "*" in domain:
            return CertDomainTypeEnum.Mixed

    return CertDomainTypeEnum.Multiple


def get_cert_brand(cert):
    org = cert.issuer.get('O')

    for cert_brand in cert_brands:
        if cert_brand in org:
            return cert_brand


def get_cert_type_by_verify_type(cert):
    """
    :param cert:
    :return:
    """
    org = cert.issuer.get('CN')
    cert_types = [
        CertTypeByVerifyWayEnum.OV,
        CertTypeByVerifyWayEnum.DV,
        CertTypeByVerifyWayEnum.EV,
    ]

    for cert_type in cert_types:
        if cert_type in org:
            return cert_type

    if cert.subject.get('O'):
        return CertTypeByVerifyWayEnum.OV

    return CertTypeByVerifyWayEnum.DV


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
            'totalDays': self.totalDays,
            'expireDays': self.expireDays,
            'certBrand': self.certBrand,
            'certTypeByVerifyWay': self.certTypeByVerifyWay,
            'certTypeByVerifyWayLabel': self.certTypeByVerifyWayLabel,
            'certTypeByDomainCount': self.certTypeByDomainCount,
            'certTypeByDomainCountLabel': self.certTypeByDomainCountLabel,
        }

    @property
    def totalDays(self):
        return time_util.get_diff_days(self.notBefore, self.notAfter)

    @property
    def expireDays(self):
        return time_util.get_diff_days(datetime.now(), self.notAfter)

    @property
    def certBrand(self):
        """
        证书品牌
        :return:
        """
        return get_cert_brand(self)

    @property
    def certTypeByDomainCountLabel(self):
        """
        域名数量
        :return:
        """
        return certTypeByDomainCountMap.get(self.certTypeByDomainCount)

    @property
    def certTypeByDomainCount(self):
        """
        域名数量
        :return:
        """
        return get_cert_type_by_domain_count(self)

    @property
    def certTypeByVerifyWay(self):
        """
        证书类型
        :return:
        """
        return get_cert_type_by_verify_type(self)

    @property
    def certTypeByVerifyWayLabel(self):
        """
        证书类型
        :return:
        """
        return CertTypeByVerifyWayEnumMap.get(self.certTypeByVerifyWay)



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


def parse_public_cert(public_cert):
    """
    解析证书信息
    :param public_cert:
    :return:
    """
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, public_cert.encode())

    return parse_cert(cert)