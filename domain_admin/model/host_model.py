# -*- coding: utf-8 -*-
"""
host_model.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, AutoField, TextField
from playhouse.shortcuts import model_to_dict

from domain_admin.config import DEFAULT_SSH_PORT
from domain_admin.enums.host_auth_type_enum import HostAuthTypeEnum
from domain_admin.model.base_model import BaseModel
from domain_admin.utils import datetime_util


class HostModel(BaseModel):
    """
    证书主机
    @since v1.5.9
    """
    id = AutoField(primary_key=True)

    # 用户id
    user_id = IntegerField(default=0)

    # 远程主机验证信息
    host = CharField(default=None, null=True)

    port = CharField(default=DEFAULT_SSH_PORT, null=True)

    user = CharField(default=None, null=True)

    # 验证方式，默认密码
    auth_type = IntegerField(default=HostAuthTypeEnum.PASSWORD)

    # CharField -> TextField
    private_key = TextField(default=None, null=True)

    password = CharField(default=None, null=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_host'

    @property
    def host_id(self):
        return self.id

    @property
    def create_time_label(self):
        return datetime_util.time_for_human(self.create_time)

    @property
    def update_time_label(self):
        return datetime_util.time_for_human(self.update_time)

    def to_hidden_dict(self):
        data = model_to_dict(
            model=self,
            extra_attrs=[
                # 'create_time_label',
                # 'update_time_label',
                'host_id',
            ],
            only=[
                HostModel.host,
                HostModel.port,
            ]
        )
        return data
