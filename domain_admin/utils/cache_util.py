# -*- coding: utf-8 -*-
"""
cache_util.py
"""
from diskcache import Cache

from domain_admin.config import CACHE_DIR

# 指定文件夹
cache = Cache(CACHE_DIR)


def set_value(key, value, expire=None):
    """
    存，单位：秒s
    """
    cache.set(key=key, value=value, expire=expire)


def get_value(key):
    """
    取
    """
    return cache.get(key=key)
