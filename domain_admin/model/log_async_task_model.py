# -*- coding: utf-8 -*-
"""
async_task_model.py
"""

from __future__ import print_function, unicode_literals, absolute_import, division

from datetime import datetime

from peewee import IntegerField, DateTimeField, TextField, AutoField, BooleanField, CharField

from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util


class AsyncTaskModel(BaseModel):
    """异步任务的执行情况记录"""
    id = AutoField(primary_key=True)

    # 用户id
    user_id = IntegerField(null=False)

    # 任务名称
    task_name = TextField(default='', null=False)

    # 函数名
    function_name = CharField(default='', null=False)

    # 执行状态: None 未执行; True 执行成功; False 执行失败
    status = BooleanField(null=True, default=None)

    # 执行结果
    result = TextField(default='', null=False)

    # 开始时间
    start_time = DateTimeField(null=True, default=None)

    # 结束时间
    end_time = DateTimeField(null=True, default=None)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'log_async_task'

    @property
    def total_time(self):
        return datetime_util.get_diff_time(self.start_time, self.end_time)

    @property
    def total_time_label(self):
        return datetime_util.seconds_for_human(self.total_time)

    @property
    def create_time_label(self):
        return datetime_util.time_for_human(self.create_time)
