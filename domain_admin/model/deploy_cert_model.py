# -*- coding: utf-8 -*-
"""
deploy_cert_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, AutoField
from playhouse.shortcuts import model_to_dict

from domain_admin.enums.deploy_status_enum import DeployStatusEnum
from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util


class DeployCertModel(BaseModel):
    """
    证书部署配置表
    @since v1.6.20
    """
    id = AutoField(primary_key=True)

    user_id = IntegerField(default=0)

    # 证书ID
    cert_id = IntegerField(default=0)

    # 部署机器
    deploy_host_id = IntegerField(default=0)

    # key部署路径
    deploy_key_file = CharField(default=None, null=True)

    # pem部署路径
    deploy_fullchain_file = CharField(default=None, null=True)

    # 部署重启命令
    deploy_reloadcmd = CharField(default=None, null=True)

    # 部署状态
    status = IntegerField(default=DeployStatusEnum.PENDING, null=False)

    # 数据版本号
    version = IntegerField(default=0, null=False)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_deploy_cert'

    @property
    def deploy_cert_id(self):
        return self.id

    @property
    def create_time_label(self):
        return datetime_util.time_for_human(self.create_time)

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)

    def to_dict(self):
        data = model_to_dict(
            model=self,
            extra_attrs=[
                'deploy_cert_id',
                'create_time_label',
                'update_time_label',
            ]
        )
        return data
