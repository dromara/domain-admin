# -*- coding: utf-8 -*-
"""
@File    : cert_openssl_v2.py
@Date    : 2023-06-19
"""
import socket
import ssl

import OpenSSL

from domain_admin.utils import domain_util, time_util


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


def verify_cert(cert, domain):
    """
    验证证书和域名是否匹配
    :param cert:
    :param domain:
    :return:
    """
    # 检查 颁发对象 域名（CN） 备用域名（SAN）
    common_name = cert.get_subject().commonName

    dns_names = get_certificate_san(cert)

    if common_name not in dns_names:
        dns_names.insert(0, common_name)

    for dns_name in dns_names:
        domain_checked = domain_util.verify_cert_common_name(dns_name, domain)
        if domain_checked:
            return True

    return False


def get_ssl_cert_by_openssl(
        domain: str,
        host: str = None,
        port: int = 443,
        timeout: int = 3):
    """
    不验证证书，仅验证域名
    支持通配符
    :param domain:
    :param host:
    :param port:
    :param timeout:
    :return:
    """
    # socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host, port))

    # ssl
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl_context.check_hostname = False

    with ssl_context.wrap_socket(sock, server_hostname=domain) as wrap_socket:
        dercert = wrap_socket.getpeercert(True)

    server_cert = ssl.DER_cert_to_PEM_cert(dercert)
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, server_cert.encode())

    # verify
    domain_checked = verify_cert(cert, domain)

    if not domain_checked:
        raise Exception("domain not verified")

    return {
        'start_date': time_util.parse_time(cert.get_notBefore().decode()),
        'expire_date': time_util.parse_time(cert.get_notAfter().decode()),
    }