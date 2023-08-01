# -*- coding: utf-8 -*-
"""
issue_certificate_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import json
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, AutoField, TextField, BooleanField

from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util
from domain_admin.utils.acme_util.challenge_type import ChallengeType

URI_ROOT_PATH = ".well-known/acme-challenge"


class IssueCertificateModel(BaseModel):
    """
    申请证书
    @since v1.5.6
    """
    id = AutoField(primary_key=True)

    # 用户id
    user_id = IntegerField(default=0)

    # SSL证书
    ssl_certificate = TextField(default=None, null=True)

    # SSL证书私钥
    ssl_certificate_key = TextField(default=None, null=True)

    # 域名列表
    domain_raw = TextField(default='')

    # 验证类型 http dns
    challenge_type = CharField(default=ChallengeType.HTTP01, null=True)

    # 域名验证token
    # @Deprecation @since v1.5.9
    token = CharField(default=None, null=True)

    # 域名验证数据
    # @Deprecation @since v1.5.9
    validation = CharField(default=None, null=True)

    # 验证状态url
    # @Deprecation @since v1.5.9
    status_url = CharField(default=None, null=True)

    # 验证状态 valid pending
    status = CharField(default='pending', null=True)

    # SSL签发时间
    start_time = DateTimeField(default=None, null=True)

    # SSL过期时间
    expire_time = DateTimeField(default=None, null=True)

    # 部署机器
    deploy_host_id = IntegerField(default=0)

    # 验证文件部署目录
    deploy_verify_path = CharField(default=None, null=True)

    # key部署路径
    deploy_key_file = CharField(default=None, null=True)

    # pem部署路径
    deploy_fullchain_file = CharField(default=None, null=True)

    # 部署重启命令
    deploy_reloadcmd = CharField(default=None, null=True)

    # 自动续期
    is_auto_renew = BooleanField(default=False)

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
    def has_ssl_certificate(self):
        """
        是否有证书文件
        :return:
        """
        return True if self.ssl_certificate else False

    @property
    def domains(self):
        if self.domain_raw:
            return json.loads(self.domain_raw)
        else:
            return []

    @property
    def domain_validation_urls(self):
        return []

        # ["http://" + domain + '/' + URI_ROOT_PATH + '/' + self.token
        # for domain in self.domains]
