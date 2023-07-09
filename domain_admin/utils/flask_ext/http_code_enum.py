# -*- coding: utf-8 -*-

"""
httpCode含义详解（转）
https://blog.csdn.net/weixin_41768263/article/details/107852135
"""
from __future__ import print_function, unicode_literals, absolute_import, division


class HttpCodeEnum(object):
    """
    HTTP 状态码
    """

    # 未授权
    Unauthorized = 401

    # 禁止访问
    Forbidden = 403

    # 未找到
    Not_Found = 404
