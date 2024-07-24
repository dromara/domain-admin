# -*- coding: utf-8 -*-
"""
issue_certificate_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import json
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, AutoField, TextField, BooleanField
from playhouse.shortcuts import model_to_dict

from domain_admin.enums.challenge_deploy_type_enum import ChallengeDeployTypeEnum
from domain_admin.enums.deploy_status_enum import DeployStatusEnum
from domain_admin.enums.ssl_deploy_type_enum import SSLDeployTypeEnum
from domain_admin.enums.valid_status_enum import ValidStatus
from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util
from domain_admin.utils.acme_util.challenge_type import ChallengeType
from domain_admin.utils.acme_util.directory_type_enum import DirectoryTypeEnum
from domain_admin.utils.acme_util.key_type_enum import KeyTypeEnum

# 常量
URI_ROOT_PATH = ".well-known/acme-challenge"


class IssueCertificateModel(BaseModel):
    """
    申请证书
    步骤：
      1、验证域名 http(ssh) dns(dns-api)
      2、签发证书
      3、部署证书 ssh api

    @since v1.5.6
    """
    id = AutoField(primary_key=True)

    # 用户id
    user_id = IntegerField(default=0)

    # 域名列表
    domain_raw = TextField(default='')

    # SSL证书
    ssl_certificate = TextField(default=None, null=True)

    # SSL证书私钥
    ssl_certificate_key = TextField(default=None, null=True)

    # SSL签发时间
    start_time = DateTimeField(default=None, null=True)

    # SSL过期时间
    expire_time = DateTimeField(default=None, null=True)

    # 证书提供商 @since v1.6.35
    directory_type = CharField(default=DirectoryTypeEnum.LETS_ENCRYPT, null=True)

    # 加密方式 @since v1.6.35
    key_type = CharField(default=KeyTypeEnum.RSA, null=True)

    # 域名验证类型 http dns
    challenge_type = CharField(default=ChallengeType.HTTP01, null=True)

    # 验证文件部署方式 ssh dns
    challenge_deploy_type_id = IntegerField(default=ChallengeDeployTypeEnum.SSH)

    # 验证文件部署账号
    challenge_deploy_id = IntegerField(default=0)

    # 验证文件部署状态
    challenge_deploy_status = IntegerField(default=DeployStatusEnum.PENDING)

    # 验证文件部署目录
    deploy_verify_path = CharField(default=None, null=True)

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
    status = CharField(default=ValidStatus.PENDING, null=True)

    # 部署方式 @since 1.6.33 可选：ssh api
    # @since 1.6.43 新增 oss
    deploy_type_id = IntegerField(default=SSLDeployTypeEnum.SSH)

    # 部署机器
    # @since 1.6.33 部署机器
    deploy_host_id = IntegerField(default=0)

    # key部署路径
    deploy_key_file = CharField(default=None, null=True)

    # pem部署路径
    deploy_fullchain_file = CharField(default=None, null=True)

    # 部署重启命令
    deploy_reloadcmd = CharField(default=None, null=True)

    # 部署请求url
    deploy_url = CharField(default=None, null=True)

    # 部署请求头
    deploy_header_raw = TextField(default=None, null=True)

    # 部署参数
    # @since 1.6.43
    deploy_params_raw = TextField(default=None, null=True)

    # ssl证书文件部署状态
    ssl_deploy_status = IntegerField(default=DeployStatusEnum.PENDING)

    # 自动续期
    is_auto_renew = BooleanField(default=False)

    # 数据版本号
    version = IntegerField(default=0, null=False)

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

    @property
    def deploy_header(self):
        if self.deploy_header_raw:
            return json.loads(self.deploy_header_raw)
        else:
            return {}

    @property
    def can_auto_renew(self):
        """
        能够选择自动续期
        :return:
        """
        return self.ssl_deploy_status == DeployStatusEnum.SUCCESS \
               and self.challenge_deploy_status == DeployStatusEnum.SUCCESS

    def to_dict(self):
        return model_to_dict(
            self,
            extra_attrs=[
                'domains',
                'create_time_label',
                'update_time_label',
                'can_auto_renew',
                'domain_validation_urls'
            ]
        )

    @property
    def deploy_params(self):
        if self.deploy_params_raw:
            return json.loads(self.deploy_params_raw)
        else:
            return {}
