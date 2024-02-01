# -*- coding: utf-8 -*-
"""
domain_icp_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, AutoField

from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util


class DomainIcpModel(BaseModel):
    """
    域名icp表 缓存icp数据
    @since 1.6.3
    """
    id = AutoField(primary_key=True)

    # 域名
    domain = CharField(null=False, unique=True)

    # 主办单位名称
    icp_company = CharField(default="")

    # ICP备案/许可证号
    icp_licence = CharField(default="")

    # 数据版本号
    version = IntegerField(default=0, null=False)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 过期时间
    expire_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_domain_icp'

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)

    @property
    def is_expired(self):
        return datetime_util.is_less_than(self.expire_time, datetime.now())
