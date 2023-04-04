# -*- coding: utf-8 -*-
"""
@File    : global_data_service.py
@Date    : 2023-04-04

APP全局数据
"""

GLOBAL_DATA = {}


def get_value(key):
    return GLOBAL_DATA.get(key)


def set_value(key, value):
    GLOBAL_DATA[key] = value


def remove_value(key):
    if key in GLOBAL_DATA:
        GLOBAL_DATA.pop(key)
