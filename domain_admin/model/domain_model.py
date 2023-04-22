# -*- coding: utf-8 -*-
import json
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, BooleanField, TextField

from domain_admin.model.base_model import BaseModel
from domain_admin.model.group_model import GroupModel
from domain_admin.utils import datetime_util


class DomainModel(BaseModel):
    """域名"""
    id = IntegerField(primary_key=True)

    # 用户id
    user_id = IntegerField(default=0)

    # 域名
    domain = CharField()

    # 别名/备注
    alias = CharField(default="")

    # ip
    ip = CharField(default="")

    # ip信息检查时间 @since 1.2.12
    ip_check_time = DateTimeField(default=None, null=True)

    # 分组
    group_id = IntegerField(default=0, null=False)

    # 域名注册时间 @since 1.1.0
    domain_start_time = DateTimeField(default=None, null=True)

    # 域名过期时间 @since 1.1.0
    domain_expire_time = DateTimeField(default=None, null=True)

    # 域名过期剩余天数，仅用于排序 @since 1.1.0
    domain_expire_days = IntegerField(default=0, null=False)

    # 域名信息检查时间 @since 1.2.12
    domain_check_time = DateTimeField(default=None, null=True)

    # SSL签发时间
    start_time = DateTimeField(default=None, null=True)

    # SSL过期时间
    expire_time = DateTimeField(default=None, null=True)

    # SSL过期剩余天数，仅用于排序
    expire_days = IntegerField(default=0, null=False)

    # 最后检查时间
    check_time = DateTimeField(default=None, null=True)

    # 连接状态
    connect_status = BooleanField(default=None, null=True)

    # 有效期总天数
    total_days = IntegerField(default=0, null=False)

    # 通知状态
    notify_status = BooleanField(default=True)

    # 是否监测 @since 1.0.3
    is_monitor = BooleanField(default=True)


    # 详细信息
    # @Deprecated
    detail_raw = TextField(default=None, null=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:

        table_name = 'tb_domain'

        indexes = (
            # 唯一索引
            (('user_id', 'domain'), True),  # Note the trailing comma!
        )

    @property
    def domain_url(self):
        return 'https://' + self.domain

    @property
    def create_time_label(self):
        return datetime_util.format_datetime_label(self.create_time)

    @property
    def check_time_label(self):
        return datetime_util.time_for_human(self.check_time)

    @property
    def start_date(self):
        if self.start_time and isinstance(self.start_time, datetime):
            return self.start_time.strftime('%Y-%m-%d')

    @property
    def expire_date(self):
        if self.expire_time and isinstance(self.expire_time, datetime):
            return self.expire_time.strftime('%Y-%m-%d')

    # @property
    # def total_days(self):
    #     if self.start_time and self.expire_time:
    #         return (self.expire_time - self.start_time).days

    @property
    def real_time_expire_days(self):
        """
        实时ssl过期剩余天数
        expire_days 是更新数据时所计算的时间，有滞后性
        :return:
        """
        if self.expire_time:
            return (self.expire_time - datetime.now()).days

    @property
    def real_time_domain_expire_days(self):
        """
        实时域名过期剩余天数
        expire_days 是更新数据时所计算的时间，有滞后性
        @since v1.1.0
        :return:
        """
        if self.domain_expire_time:
            return (self.domain_expire_time - datetime.now()).days

    @property
    def detail(self):
        if self.detail_raw:
            return json.loads(self.detail_raw)

    @property
    def group(self):
        if self.group_id:
            return GroupModel.get_or_none(GroupModel.id == self.group_id)
