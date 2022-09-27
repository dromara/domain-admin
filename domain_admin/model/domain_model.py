# -*- coding: utf-8 -*-
import json
from datetime import datetime
from domain_admin.model import GroupModel
from domain_admin.model.base_model import BaseModel
from peewee import CharField, IntegerField, DateTimeField, BooleanField, TextField


class DomainModel(BaseModel):
    """域名"""
    id = IntegerField(primary_key=True)

    # 域名
    domain = CharField()

    # 别名
    alias = CharField(default="")

    # ip
    ip = CharField(default="")

    # 分组
    group_id = IntegerField(default=0)

    # 签发时间
    start_time = DateTimeField(default=None, null=True)

    # 过期时间
    expire_time = DateTimeField(default=None, null=True)

    # 连接状态
    connect_status = BooleanField(default=False, null=True)

    # 通知状态
    notify_status = BooleanField(default=True)

    # 最后检查时间
    check_time = DateTimeField(default=None, null=True)

    # 详细信息
    detail_raw = TextField(default=None, null=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    @property
    def start_date(self):
        if self.start_time and isinstance(self.start_time, datetime):
            return self.start_time.strftime('%Y-%m-%d')

    @property
    def expire_date(self):
        if self.expire_time and isinstance(self.expire_time, datetime):
            return self.expire_time.strftime('%Y-%m-%d')

    @property
    def total_days(self):
        if self.start_time and self.expire_time:
            return (self.expire_time - self.start_time).days

    @property
    def expire_days(self):
        if self.expire_time:
            return (self.expire_time - datetime.now()).days

    @property
    def detail(self):
        if self.detail_raw:
            return json.loads(self.detail_raw)

    @property
    def group(self):
        if self.group_id:
            return GroupModel.get_or_none(GroupModel.id == self.group_id)
