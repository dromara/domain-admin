# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, AutoField

from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util


class LogMonitorModel(BaseModel):
    """监控日志"""
    id = AutoField(primary_key=True)

    # id
    monitor_id = IntegerField(default=0)

    # 监控类型
    monitor_type = IntegerField(default=0)

    # 状态
    status = IntegerField(default=0)

    # 结果
    result = CharField(default='')

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_log_monitor'

    @property
    def create_time_label(self):
        return datetime_util.format_datetime_label(self.create_time)

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)
