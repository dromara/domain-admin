# -*- coding: utf-8 -*-
"""
@File    : cert_openssl_v2.py
@Date    : 2023-06-19
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import socket
import ssl

import OpenSSL
from OpenSSL.crypto import X509

from domain_admin.enums.ssl_type_enum import SSLTypeEnum
from domain_admin.utils import domain_util, time_util, json_util
from domain_admin.utils.cert_util import cert_common

# 默认的ssl端口
DEFAULT_SSL_PORT = 443


def verify_cert(cert, domain):
    """
    验证证书和域名是否匹配
    :param cert:
    :param domain:
    :return:
    """
    # 检查 颁发对象 域名（CN） 备用域名（SAN）
    common_name = cert.get_subject().commonName

    dns_names = cert_common.get_certificate_san(cert)

    if common_name not in dns_names:
        dns_names.insert(0, common_name)

    for dns_name in dns_names:
        domain_checked = domain_util.verify_cert_common_name(dns_name, domain)
        if domain_checked:
            return True

    return False


def get_ssl_cert(
        domain,
        host=None,
        port=443,
        timeout=3,
        ssl_type=SSLTypeEnum.SSL_TLS
):
    """
    不验证证书，仅验证域名
    支持通配符
    :param ssl_type:
    :param domain: str
    :param host: str
    :param port: int
    :param timeout: int
    :return:
    """
    # 默认参数
    host = host or domain

    # socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host, port))

    # 用户可以设置使用协议：STARTTLS、SSL/TLS
    # issues: https://github.com/mouday/domain-admin/issues/57
    # ref: https://stackoverflow.com/questions/5108681/use-python-to-get-an-smtp-server-certificate/62695088#62695088
    # ref: https://serverfault.com/questions/131627/how-to-inspect-remote-smtp-servers-tls-certificate#:~:text=If%20you%20don%27t%20have%20OpenSSL%2C%20you%20can%20also,ssl.DER_cert_to_PEM_cert%20%28connection.sock.getpeercert%20%28binary_form%3DTrue%29%29%20where%20%5Bhostname%5D%20is%20the%20server.
    if ssl_type == SSLTypeEnum.START_TLS:
        try:
            sock.recv(1000)
            sock.send('EHLO\nSTARTTLS\n'.encode('utf-8'))
            sock.recv(1000)
        except:
            pass

    # ssl
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl_context.check_hostname = False

    # fix: Python2 AttributeError: __exit__
    wrap_socket = ssl_context.wrap_socket(sock, server_hostname=domain)
    dercert = wrap_socket.getpeercert(True)
    wrap_socket.close()

    server_cert = ssl.DER_cert_to_PEM_cert(dercert)
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, server_cert.encode())
    return cert


def get_ssl_cert_by_openssl(
        domain,
        host=None,
        port=443,
        timeout=3,
        ssl_type=SSLTypeEnum.SSL_TLS
):
    """
    不验证证书，仅验证域名
    支持通配符
    :param ssl_type:
    :param domain: str
    :param host: str
    :param port: int
    :param timeout: int
    :return:
    """

    cert = get_ssl_cert(domain, host, port, timeout, ssl_type=ssl_type)

    # verify
    domain_checked = verify_cert(cert, domain)

    if not domain_checked:
        raise Exception("domain not verified")

    return {
        'start_date': time_util.parse_time(cert.get_notBefore().decode()),
        'expire_date': time_util.parse_time(cert.get_notAfter().decode()),
    }
