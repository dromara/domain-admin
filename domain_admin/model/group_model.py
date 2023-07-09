# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, AutoField

from domain_admin.model.base_model import BaseModel


class GroupModel(BaseModel):
    """分组"""
    id = AutoField(primary_key=True)

    # 名称
    name = CharField()

    # 用户id
    user_id = IntegerField(default=0)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_group'
