# -*- coding: utf-8 -*-
"""
@File    : monitor_status_enum.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division


class MonitorStatusEnum(object):
    """
    监控状态枚举值
    """
    # 未知
    UNKNOWN = 0

    # 成功
    SUCCESS = 1

    # 失败
    ERROR = 2
