# -*- coding: utf-8 -*-
"""
log_monitor_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, AutoField

from domain_admin.enums.monitor_status_enum import MonitorStatusEnum
from domain_admin.enums.monitor_type_enum import MonitorTypeEnum
from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util
from domain_admin.utils.peewee_ext.field import MyDateTimeField


class LogMonitorModel(BaseModel):
    """监控日志"""
    id = AutoField(primary_key=True)

    # id
    monitor_id = IntegerField(default=0)

    # 监控类型
    monitor_type = IntegerField(default=MonitorTypeEnum.UNKNOWN)

    # 状态
    status = IntegerField(default=MonitorStatusEnum.UNKNOWN)

    # 结果
    result = CharField(default='')

    # 创建时间
    create_time = MyDateTimeField(default=datetime.now)

    # 更新时间
    update_time = MyDateTimeField(default=None, null=True)

    class Meta:
        table_name = 'tb_log_monitor'

    @property
    def create_time_label(self):
        return datetime_util.format_datetime_label(self.create_time)

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)

    @property
    def total_microsecond_time(self):
        end_time = self.update_time or datetime.now()
        return datetime_util.get_diff_time_with_microsecond(self.create_time, end_time)

    @property
    def total_time_label(self):
        return datetime_util.microsecond_for_human(self.total_microsecond_time)
