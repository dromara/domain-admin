# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
"""
group_user_model.py
"""
from datetime import datetime

from peewee import IntegerField, DateTimeField, AutoField, BooleanField

from domain_admin.model.base_model import BaseModel


class GroupUserModel(BaseModel):
    """分组成员表"""
    id = AutoField(primary_key=True)

    # 分组id
    group_id = IntegerField(default=0)

    # 用户id
    user_id = IntegerField(default=0)

    # 写操作权限
    has_edit_permission = BooleanField(default=False)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_group_user'

        indexes = (
            # 唯一索引
            (('group_id', 'user_id'), True),  # Note the trailing comma!
        )
