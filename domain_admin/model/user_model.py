# -*- coding: utf-8 -*-
import json
from datetime import datetime

from domain_admin.config import ADMIN_USERNAME
from domain_admin.model.base_model import BaseModel
from peewee import CharField, IntegerField, DateTimeField, BooleanField, TextField

from domain_admin.utils import bcrypt_util


class UserModel(BaseModel):
    """用户"""
    id = IntegerField(primary_key=True)

    # 用户名
    username = CharField(unique=True, null=None)

    # 密码
    password = CharField()

    # 头像
    avatar_url = CharField(null=None, default='')

    # 过期前多少天提醒
    before_expire_days = IntegerField(null=None, default=3)

    # 邮件列表
    email_list_raw = TextField(default=None, null=True)

    # 账号状态
    status = BooleanField(default=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_user'

    @property
    def email_list(self):
        if self.email_list_raw:
            return json.loads(self.email_list_raw)
        else:
            return []


def init_table_data():
    data = [
        {
            'username': ADMIN_USERNAME,
            'password': bcrypt_util.encode_password('123456'),
            'before_expire_days': 3,
        }
    ]

    UserModel.insert_many(data).execute()
