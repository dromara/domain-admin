# -*- coding: utf-8 -*-
"""
issue_certificate_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import json
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, BooleanField, AutoField, TextField

from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util, time_util

URI_ROOT_PATH = ".well-known/acme-challenge"


class IssueCertificateModel(BaseModel):
    """
    申请证书
    @since v1.5.6
    """
    id = AutoField(primary_key=True)

    # 用户id
    user_id = IntegerField(default=0)

    # 域名列表
    domain_raw = TextField()

    # SSL证书
    ssl_certificate = TextField(default=None, null=True)

    # SSL证书私钥
    ssl_certificate_key = TextField(default=None, null=True)

    # 域名验证token
    token = CharField(default=None, null=True)

    # 域名验证数据
    validation = CharField(default=None, null=True)

    # 验证状态url
    status_url = CharField(default=None, null=True)

    # 验证状态 valid pending
    status = CharField(default=None, null=True)

    # SSL签发时间
    start_time = DateTimeField(default=None, null=True)

    # SSL过期时间
    expire_time = DateTimeField(default=None, null=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:

        table_name = 'tb_issue_certificate'

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
    def challenge_url(self):
        return '/.well-known/acme-challenge/{}'.format(self.token)

    @property
    def domains(self):
        return json.loads(self.domain_raw)

    @property
    def domain_validation_urls(self):
        return [
            "http://" + domain + '/' + URI_ROOT_PATH + '/' + self.token
            for domain in self.domains]
