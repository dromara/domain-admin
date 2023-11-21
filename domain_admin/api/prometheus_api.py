# -*- coding: utf-8 -*-
"""
@File    : prometheus_api.py
@Date    : 2023-06-30
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import re

import prometheus_client
from flask import Response, request
from flask import current_app
from playhouse.shortcuts import model_to_dict
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry

from domain_admin.config import PROMETHEUS_KEY
from domain_admin.enums.config_key_enum import ConfigKeyEnum
from domain_admin.log import logger
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.service import group_service


def metrics():
    """
    prometheus metrics接口
    :return:
    """
    # 鉴权
    logger.info('metrics')

    authorization = request.headers.get('Authorization')
    ret = re.match('Bearer (?P<token>.*)', authorization)
    token = ret.groupdict().get('token')

    prometheus_key = current_app.config[ConfigKeyEnum.PROMETHEUS_KEY]

    if token != prometheus_key:
        return Response("Unauthorized", status=401)

    registry = CollectorRegistry(auto_describe=False)

    # 证书数据
    gauge = Gauge(
        "domain_admin",
        "this is a domain admin data",
        ["domain", "root_domain", "group_name"],
        registry=registry)

    rows = DomainModel.select()

    lst = [model_to_dict(row, extra_attrs=['real_time_expire_days']) for row in rows]

    # 分组名
    group_service.load_group_name(lst)
    logger.info('group_service a')
    for row in lst:
        gauge.labels(
            row['domain'],
            row['root_domain'],
            row['group_name']
        ).set(row['real_time_expire_days'])

    logger.info('success')

    # 域名数据 @since v1.5.27
    domain_info_fields = [
        "id",
        "user_id",
        "domain",
        "group_id",
        "group_name",
        "comment",
        "domain_registrar",
        "domain_registrar_url",
        "domain_start_time",
        "domain_expire_time",
        "is_auto_update",
        "is_expire_monitor",
        "icp_company",
        "icp_licence",
        'tags',
        'real_domain_expire_days',
        'update_time_label',
        'domain_start_date',
        'domain_expire_date',
        "create_time",
        "update_time",
    ]

    domain_info_gauge = Gauge(
        name="domain_info",
        documentation="this is a domain info data",
        labelnames=domain_info_fields,
        registry=registry)

    domain_info_rows = DomainInfoModel.select()

    domain_info_lst = [model_to_dict(
        row,
        extra_attrs=[
            'tags',
            'real_domain_expire_days',
            'update_time_label',
            'domain_start_date',
            'domain_expire_date',
        ]
    ) for row in domain_info_rows]

    # 分组名
    group_service.load_group_name(domain_info_lst)
    for row in domain_info_lst:
        domain_info_gauge.labels(
            *[row[field] for field in domain_info_fields]
        ).set(row['real_domain_expire_days'])

    return Response(prometheus_client.generate_latest(registry), mimetype='text/plain')
