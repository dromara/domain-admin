# -*- coding: utf-8 -*-
"""
log_operation_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from datetime import datetime

from peewee import DateTimeField, TextField, AutoField, IntegerField, CharField

from domain_admin.enums.operation_enum import OperationEnum
from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util


class LogOperationModel(BaseModel):
    """操作日志"""
    id = AutoField(primary_key=True)

    # 用户id
    user_id = IntegerField(null=False)

    # 操作表
    table = CharField(default='')

    # 操作类型id
    type_id = IntegerField(default=0, null=False)

    # 操作之前
    before = TextField(default='')

    # 操作之后
    after = TextField(default='')

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'log_operation'

    @property
    def create_time_label(self):
        return datetime_util.time_for_human(self.create_time)

    @property
    def type_label(self):
        return OperationEnum.get_label(self.type_id)
