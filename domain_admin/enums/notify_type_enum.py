# -*- coding: utf-8 -*-
"""
@File    : notify_type_enum.py
@Date    : 2022-10-30
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division

class NotifyTypeEnum(object):
    """
    通知方式枚举值
    """
    # 未知
    Unknown = 0

    # 邮件
    Email = 1

    # webHook
    WebHook = 2

    # 企业微信
    WORK_WEIXIN = 3

    # 钉钉
    DING_TALK = 4

    # 飞书
    FEISHU = 5
