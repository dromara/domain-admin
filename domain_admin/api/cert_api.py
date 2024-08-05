# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

from flask import request, Response

from domain_admin.enums.role_enum import RoleEnum
from domain_admin.service import auth_service, cert_service
from domain_admin.utils import domain_util
from domain_admin.utils.cert_util import cert_openssl_v2, cert_common


@auth_service.permission(role=RoleEnum.USER)
def get_cert_information():
    """
    获取域名证书信息
    :return:
    """
    if request.method == 'GET':
        domain = request.args['domain']
    else:
        domain = request.json['domain']

    # 解析域名
    return cert_service.get_cert_information(domain=domain)


@auth_service.permission(role=RoleEnum.USER)
def parse_public_cert():
    certificate = request.json['certificate']
    parsed_cert = cert_common.parse_public_cert(certificate)
    return parsed_cert.to_dict() if parsed_cert else parsed_cert
