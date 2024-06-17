# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, AutoField

from domain_admin.enums.dns_type_enum import DnsTypeEnum
from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util


class DnsModel(BaseModel):
    """DNS账号"""
    id = AutoField(primary_key=True)

    # 用户id
    user_id = IntegerField(default=0)

    # 类型
    dns_type_id = IntegerField(null=False, default=DnsTypeEnum.ALIYUN)

    # 名称
    name = CharField()

    # Access Key
    access_key = CharField()

    # Secret Key
    secret_key = CharField()

    # 数据版本号
    version = IntegerField(default=0, null=False)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_dns'

    @property
    def create_time_label(self):
        return datetime_util.format_datetime_label(self.create_time)

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)
