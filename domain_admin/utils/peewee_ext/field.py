# -*- coding: utf-8 -*-
"""
@File    : field.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""
from peewee import DateTimeField



class MyDateTimeField(DateTimeField):
    """
    peewee datetime字段至微秒
    https://www.cnpython.com/qa/1516384
    """
    def get_modifiers(self):
        return [6]
