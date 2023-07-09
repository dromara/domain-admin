# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
import json
from datetime import datetime

from peewee import IntegerField, DateTimeField, TextField, AutoField, BooleanField

from domain_admin.config import DEFAULT_BEFORE_EXPIRE_DAYS
from domain_admin.enums.event_enum import EventEnum
from domain_admin.enums.notify_type_enum import NotifyTypeEnum
from domain_admin.model.base_model import BaseModel


class NotifyModel(BaseModel):
    """通知配置"""
    id = AutoField(primary_key=True)

    # 用户id
    user_id = IntegerField(null=False)

    # 事件分类
    event_id = IntegerField(null=False, default=EventEnum.SSL_CERT_EXPIRE)

    # 通知方式
    type_id = IntegerField(null=False, default=NotifyTypeEnum.Unknown)

    # 过期剩余天数
    expire_days = IntegerField(null=False, default=DEFAULT_BEFORE_EXPIRE_DAYS)

    # 原始值
    value_raw = TextField(default=None, null=True)

    # 启用状态
    status = BooleanField(null=False, default=True)

    # 备注说明
    comment = TextField(default='', null=False)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_notify'

        # 移除唯一索引
        # indexes = (
        #     # 唯一索引
        #     (('user_id', 'type_id'), True),
        # )

    @property
    def value(self):
        if self.value_raw:
            return json.loads(self.value_raw)
        else:
            return None

    # email参数
    @property
    def email_list(self):
        if self.value:
            return self.value.get('email_list')

    # webhook参数
    @property
    def webhook_method(self):
        if self.value:
            return self.value.get('method')

    @property
    def webhook_url(self):
        if self.value:
            return self.value.get('url')

    @property
    def webhook_headers(self):
        if self.value:
            return self.value.get('headers')

    @property
    def webhook_body(self):
        if self.value:
            return self.value.get('body')

    # 企业微信参数
    @property
    def work_weixin_corpid(self):
        if self.value:
            return self.value.get('corpid')

    @property
    def work_weixin_corpsecret(self):
        if self.value:
            return self.value.get('corpsecret')

    @property
    def work_weixin_body(self):
        if self.value:
            return self.value.get('body')

    # dingtalk
    @property
    def ding_talk_appkey(self):
        if self.value:
            return self.value.get('appkey')

    @property
    def ding_talk_appsecret(self):
        if self.value:
            return self.value.get('appsecret')

    @property
    def ding_talk_body(self):
        if self.value:
            return self.value.get('body')

    # 飞书
    @property
    def feishu_body(self):
        if self.value:
            return self.value.get('body')

    @property
    def feishu_params(self):
        if self.value:
            return self.value.get('params')

    @property
    def feishu_app_id(self):
        if self.value:
            return self.value.get('app_id')

    @property
    def feishu_app_secret(self):
        if self.value:
            return self.value.get('app_secret')
