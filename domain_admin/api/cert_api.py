# -*- coding: utf-8 -*-
from flask import request

from domain_admin.utils import cert_util_v2


def get_cert_information():
    """
    获取域名证书信息
    :return:
    """
    if request.method == 'GET':
        domain = request.args['domain']
    else:
        domain = request.json['domain']

    try:
        data = cert_util_v2.get_cert_info(domain)
    except Exception as e:
        data = None

    return data
