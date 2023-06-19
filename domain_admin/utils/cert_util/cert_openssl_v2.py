# -*- coding: utf-8 -*-
"""
@File    : demo.py
@Date    : 2023-06-19
"""
import socket
import ssl

import OpenSSL

from domain_admin.utils.cert_util import cert_common


def get_ssl_cert_by_openssl(domain: str, host: str = None, port: int = 443, timeout: int = 3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((host, port))

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

    with ssl_context.wrap_socket(sock, server_hostname=domain) as wrap_socket:
        dercert = wrap_socket.getpeercert(True)

    server_cert = ssl.DER_cert_to_PEM_cert(dercert)
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, server_cert.encode())

    return {
        'start_date': cert_common.parse_time(cert.get_notBefore().decode()),
        'expire_date': cert_common.parse_time(cert.get_notAfter().decode()),
    }


if __name__ == '__main__':
    # get_ssl_cert_by_openssl('pgmanage.qnvip.com', '121.196.205.251')
    # get_ssl_cert_by_openssl('cdn-image-01.kaishuleyuan.com', '101.96.145.100')
    get_ssl_cert_by_openssl('dev.csdn.net', '120.46.209.149')
