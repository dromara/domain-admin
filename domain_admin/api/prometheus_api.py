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
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry

from domain_admin.config import PROMETHEUS_KEY
from domain_admin.enums.config_key_enum import ConfigKeyEnum
from domain_admin.log import logger
from domain_admin.model.domain_model import DomainModel


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

    gauge = Gauge(
        "domain_admin",
        "this is a domain admin data",
        ["domain"],
        registry=registry)

    rows = DomainModel.select()

    for row in rows:
        gauge.labels(row.domain).set(row.real_time_expire_days)

    logger.info('success')

    return Response(prometheus_client.generate_latest(registry), mimetype='text/plain')
