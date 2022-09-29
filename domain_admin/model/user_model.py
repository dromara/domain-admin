# -*- coding: utf-8 -*-
import json
from datetime import datetime

from domain_admin.model.base_model import BaseModel
from peewee import CharField, IntegerField, DateTimeField, BooleanField, TextField


class UserModel(BaseModel):
    """用户"""
    id = IntegerField(primary_key=True)

    # 用户名
    username = CharField()

    # 密码
    password = CharField()

    # 过期前多少天提醒
    before_expire_days = IntegerField(default=0)

    # 邮件列表
    email_list_raw = TextField(default=None, null=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    @property
    def email_list(self):
        if self.email_list_raw:
            return json.loads(self.email_list_raw)
