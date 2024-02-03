# -*- coding: utf-8 -*-
"""
tag_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from datetime import datetime

from peewee import DateTimeField, AutoField, TextField, CharField

from domain_admin.model.base_model import BaseModel


class TagModel(BaseModel):
    """标签表
    """
    id = AutoField(primary_key=True)

    # 标签名
    name = CharField(default='', null=False, unique=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_tag'
