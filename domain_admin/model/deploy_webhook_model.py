# -*- coding: utf-8 -*-
"""
deploy_webhook_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import json
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, AutoField
from playhouse.shortcuts import model_to_dict

from domain_admin.enums.deploy_status_enum import DeployStatusEnum
from domain_admin.enums.object_enum import ObjectEnum
from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util


class DeployWebhookModel(BaseModel):
    """
    api方式部署证书配置表
    @since v1.6.52
    """
    id = AutoField(primary_key=True)

    user_id = IntegerField(default=0)

    # 证书ID
    object_id = IntegerField(default=0)

    # 证书类型
    object_type = IntegerField(default=ObjectEnum.Certificate)

    # 部署url
    url = CharField(default=None, null=True)

    # 头部
    header_raw = CharField(default=None, null=True)

    # 部署状态
    status = IntegerField(default=DeployStatusEnum.PENDING, null=False)

    # 数据版本号
    version = IntegerField(default=0, null=False)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_deploy_webhook'

    @property
    def deploy_webhook_id(self):
        return self.id

    @property
    def create_time_label(self):
        return datetime_util.time_for_human(self.create_time)

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)

    @property
    def headers(self):
        if self.header_raw:
            return json.loads(self.header_raw)
        else:
            return {}

    def to_dict(self):
        data = model_to_dict(
            model=self,
            extra_attrs=[
                'deploy_webhook_id',
                'create_time_label',
                'update_time_label',
                'headers',
            ]
        )
        return data
