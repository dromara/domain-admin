# -*- coding: utf-8 -*-
from datetime import datetime

from domain_admin.model.base_model import BaseModel
from peewee import CharField, IntegerField, DateTimeField, BooleanField


class DomainModel(BaseModel):
    """域名"""
    id = IntegerField(primary_key=True)

    # 域名
    domain = CharField()

    # 别名
    alias = CharField(default="")

    # 分组
    group_id = IntegerField(default=0)

    # 签发时间
    start_time = DateTimeField(default=None, null=True)

    # 过期时间
    expire_time = DateTimeField(default=None, null=True)

    # 连接状态
    connect_status = BooleanField(default=False, null=True)

    # 最后检查时间
    check_time = DateTimeField(default=None, null=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)
