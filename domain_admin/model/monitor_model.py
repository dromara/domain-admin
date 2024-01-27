# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, BooleanField, AutoField, TextField

from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util


class MonitorModel(BaseModel):
    """监控"""
    id = AutoField(primary_key=True)

    # 用户id
    user_id = IntegerField(default=0)

    # 名称
    title = CharField(default='')

    # 监控类型
    monitor_type = IntegerField(default=0)

    # 监控参数
    # http {url, method, timeout}
    content = TextField(default=None)

    # 间隔 检测频率
    interval = IntegerField(default=60)

    # 允许失败次数
    allow_error_count = IntegerField(default=0)

    # 状态
    status = IntegerField(default=0)

    # 是否监测
    is_monitor = BooleanField(default=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_monitor'

    @property
    def create_time_label(self):
        return datetime_util.format_datetime_label(self.create_time)

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)
