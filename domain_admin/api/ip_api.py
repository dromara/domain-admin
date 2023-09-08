# -*- coding: utf-8 -*-
"""
@File    : ip_api.py
@Date    : 2022-10-14
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from flask import request

from domain_admin.utils import ip_util, dns_util


def get_ip_info():
    """
    获取ip地址的信息
    :return:
    """
    ip = request.json['ip']
    return ip_util.get_ip_info(ip)


def query_domain_cname():
    """
    查询域名的CNAME记录
    :return:
    """
    domain = request.json['domain']
    return dns_util.query_domain_cname(domain)
