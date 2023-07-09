# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, BooleanField, AutoField

from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util, time_util


class AddressModel(BaseModel):
    """
    域名主机ip地址
    @since v1.2.24
    """
    id = AutoField(primary_key=True)

    # 域名
    domain_id = CharField(null=False)

    # 主机地址
    host = CharField(default="")

    # SSL签发时间
    ssl_start_time = DateTimeField(default=None, null=True)

    # SSL过期时间
    ssl_expire_time = DateTimeField(default=None, null=True)

    # SSL过期剩余天数，仅用于排序
    ssl_expire_days = IntegerField(default=0, null=False)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:

        table_name = 'tb_address'

        indexes = (
            # 唯一索引
            (('domain_id', 'host'), True),  # Note the trailing comma!
        )

    @property
    def create_time_label(self):
        return datetime_util.format_datetime_label(self.create_time)

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)

    @property
    def ssl_start_date(self):
        if self.ssl_start_time and isinstance(self.ssl_start_time, datetime):
            return self.ssl_start_time.strftime('%Y-%m-%d')

    @property
    def ssl_expire_date(self):
        if self.ssl_expire_time and isinstance(self.ssl_expire_time, datetime):
            return self.ssl_expire_time.strftime('%Y-%m-%d')

    @property
    def real_time_ssl_expire_days(self):
        """
        实时ssl过期剩余天数
        ssl_expire_days 是更新数据时所计算的时间，有滞后性
        :return:
        """
        return time_util.get_diff_days(datetime.now(), self.ssl_expire_time)
