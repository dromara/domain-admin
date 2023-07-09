# -*- coding: utf-8 -*-
"""
@File    : status_enum.py
@Date    : 2022-10-30
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division

class StatusEnum(object):
    """
    数据状态枚举值
    """
    # 隐藏/禁用 disabled
    Disabled = 0

    # 公开/生效 enabled
    Enabled = 1
