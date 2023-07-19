# -*- coding: utf-8 -*-
"""
domain_info_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import json
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, AutoField, BooleanField, TextField

from domain_admin.model.base_model import BaseModel
from domain_admin.utils import time_util, datetime_util


class DomainInfoModel(BaseModel):
    """
    域名信息表
    @since 1.4.0
    """
    id = AutoField(primary_key=True)

    # 用户id
    user_id = IntegerField(null=False)

    # 分组
    group_id = IntegerField(default=0, null=False)

    # 备注
    comment = CharField(default="")

    # 域名
    domain = CharField(null=False)

    # 域名注册商
    domain_registrar = CharField(default="")

    # 域名注册商地址
    domain_registrar_url = CharField(default="")

    # 域名注册时间
    domain_start_time = DateTimeField(default=None, null=True)

    # 域名过期时间
    domain_expire_time = DateTimeField(default=None, null=True)

    # 域名过期剩余天数，仅用于排序
    domain_expire_days = IntegerField(default=0, null=False)

    # 域名信息自动更新
    is_auto_update = BooleanField(default=True)

    # 域名过期监测
    is_expire_monitor = BooleanField(default=True)

    # 主办单位名称 @since 1.5.2
    icp_company = CharField(default="")

    # ICP备案/许可证号 @since 1.5.2
    icp_licence = CharField(default="")

    # 标签list @since 1.5.2
    tags_raw = TextField(default=None, null=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_domain_info'

        indexes = (
            # 唯一索引
            (('user_id', 'domain'), True),  # Note the trailing comma!
        )

    @property
    def domain_start_date(self):
        if self.domain_start_time and isinstance(self.domain_start_time, datetime):
            return self.domain_start_time.strftime('%Y-%m-%d')

    @property
    def domain_expire_date(self):
        if self.domain_expire_time and isinstance(self.domain_expire_time, datetime):
            return self.domain_expire_time.strftime('%Y-%m-%d')

    @property
    def real_domain_expire_days(self):
        """
        域名过期天数，用于前端显示
        :return: int
        """
        return time_util.get_diff_days(datetime.now(), self.domain_expire_time)

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)

    @property
    def tags(self):
        if self.tags_raw:
            return json.loads(self.tags_raw)

    @tags.setter
    def tags(self, value):
        self.tags_raw = json.dumps(value, ensure_ascii=False)

    @property
    def tags_str(self):
        if self.tags:
            return '、'.join(self.tags)
