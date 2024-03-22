# -*- coding: utf-8 -*-
"""
certificate_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from datetime import datetime

from peewee import IntegerField, DateTimeField, AutoField, TextField, CharField
from playhouse.shortcuts import model_to_dict

from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util, time_util


class CertificateModel(BaseModel):
    """
    证书托管表
    @since v1.6.12
    """
    id = AutoField(primary_key=True)

    # 用户id
    user_id = IntegerField(default=0)

    # 域名
    domain = CharField(null=False)

    # SSL证书
    ssl_certificate = TextField(default=None, null=True)

    # SSL证书私钥
    ssl_certificate_key = TextField(default=None, null=True)

    # SSL签发时间
    start_time = DateTimeField(default=None, null=True)

    # SSL过期时间
    expire_time = DateTimeField(default=None, null=True)

    # 备注
    comment = CharField(default="")

    # 数据版本号
    version = IntegerField(default=0, null=False)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:

        table_name = 'tb_certificate'

    @property
    def certificate_id(self):
        return self.id

    @property
    def create_time_label(self):
        return datetime_util.time_for_human(self.create_time)

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)

    @property
    def start_date(self):
        if self.start_time and isinstance(self.start_time, datetime):
            return self.start_time.strftime('%Y-%m-%d')

    @property
    def expire_date(self):
        if self.expire_time and isinstance(self.expire_time, datetime):
            return self.expire_time.strftime('%Y-%m-%d')

    @property
    def real_time_expire_days(self):
        """
        实时ssl过期剩余天数
        expire_days 是更新数据时所计算的时间，有滞后性
        :return: int
        """
        return time_util.get_diff_days(datetime.now(), self.expire_time)

    def to_dict(self):
        data = model_to_dict(
            model=self,
            extra_attrs=[
                'create_time_label',
                'update_time_label',
                'real_time_expire_days',
                'start_date',
                'expire_date',
                'certificate_id',
            ]
        )

        return data
