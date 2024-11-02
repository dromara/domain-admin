# -*- coding: utf-8 -*-
"""
monitor_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import json
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, BooleanField, AutoField, TextField
from playhouse.shortcuts import model_to_dict

from domain_admin.enums.monitor_status_enum import MonitorStatusEnum
from domain_admin.enums.monitor_type_enum import MonitorTypeEnum
from domain_admin.enums.time_unit_enum import TimeUnitEnum
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
    monitor_type = IntegerField(default=MonitorTypeEnum.UNKNOWN)

    # 监控参数
    # http {url, method, timeout}
    # @since v1.6.56 add timeout_unit
    content = TextField(default=None)

    # 间隔 检测频率
    interval = IntegerField(default=60)

    # 间隔 检测频率单位：默认：分钟
    interval_unit = IntegerField(default=TimeUnitEnum.Minute)

    # 允许失败次数
    allow_error_count = IntegerField(default=0)

    # 状态
    status = IntegerField(default=MonitorStatusEnum.UNKNOWN)

    # 是否监测
    is_active = BooleanField(default=True)

    # 下一次运行时间
    next_run_time = DateTimeField(default=None, null=True)

    # 数据版本号 @since 1.6.11
    version = IntegerField(default=0, null=False)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=None, null=True)

    class Meta:
        table_name = 'tb_monitor'

    @property
    def monitor_id(self):
        return self.id

    @property
    def create_time_label(self):
        return datetime_util.format_datetime_label(self.create_time)

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)

    @property
    def content_dict(self):
        return json.loads(self.content)

    @property
    def http_url(self):
        return self.content_dict.get('url')

    @property
    def http_timeout(self):
        return int(self.content_dict.get('timeout'))

    @property
    def http_timeout_unit(self):
        return self.content_dict.get('timeout_unit')

    @property
    def http_timeout_unit_label(self):
        return TimeUnitEnum.get_label(self.http_timeout_unit)

    @property
    def interval_unit_label(self):
        return TimeUnitEnum.get_label(self.interval_unit)

    def to_dict(self):
        data = model_to_dict(
            model=self,
            extra_attrs=[
                'create_time_label',
                'update_time_label',
                'content_dict',
                'monitor_id',
                'http_url',
                'http_timeout',
                'http_timeout_unit',
                'http_timeout_unit_label',
                'interval_unit_label',
            ]
        )

        data['content'] = data.pop('content_dict')
        return data


# 数据导入导出字段关系
FIELD_MAPPING = [
    {
        'name': '名称',
        'field': 'title',
    },
    {
        'name': '请求URL',
        'field': 'http_url',
    },
    {
        'name': '请求超时',
        'field': 'http_timeout',
    },
    {
        'name': '请求超时单位',
        'field': 'http_timeout_unit_label',
    },
    {
        'name': '检测频率',
        'field': 'interval',
    },
    {
        'name': '检测频率单位',
        'field': 'interval_unit_label',
    },
]
