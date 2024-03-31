# -*- coding: utf-8 -*-
"""
@File    : deploy_status_enum.py
@Date    : 2024-03-31
"""

from __future__ import print_function, unicode_literals, absolute_import, division


class DeployStatusEnum(object):
    """
    部署状态枚举值
    """
    # 等待部署 默认
    PENDING = 0

    # 部署成功
    SUCCESS = 1

    # 部署失败
    ERROR = 2
