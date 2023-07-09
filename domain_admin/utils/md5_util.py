# -*- coding: utf-8 -*-
"""
@File    : md5_util.py
@Date    : 2023-06-30
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import hashlib


def md5(msg):
    """
    获取字符串的md5值
    :param msg:
    :return: str
    """
    return hashlib.md5(msg.encode("utf-8")).hexdigest()
