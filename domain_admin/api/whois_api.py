# -*- coding: utf-8 -*-
"""
@File    : whois_api.py
@Date    : 2023-06-01
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from flask import request

from domain_admin.enums.role_enum import RoleEnum
from domain_admin.service import auth_service
from domain_admin.utils import whois_util


@auth_service.permission(role=RoleEnum.USER)
def get_whois_raw():
    """
    获取域名信息原始
    :return:
    """
    domain = request.json['domain']
    resolve_domain = whois_util.resolve_domain(domain)
    raw_data = whois_util.get_domain_raw_whois(resolve_domain)

    return {
        "domain": domain,
        "resolve_domain": resolve_domain,
        "raw_data": raw_data
    }
