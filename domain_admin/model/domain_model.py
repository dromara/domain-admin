# -*- coding: utf-8 -*-
import json
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, BooleanField, TextField

from domain_admin.model.base_model import BaseModel
from domain_admin.model.group_model import GroupModel
from domain_admin.utils import datetime_util, time_util


class DomainModel(BaseModel):
    """域名"""
    id = IntegerField(primary_key=True)

    # 用户id
    user_id = IntegerField(default=0)

    # 域名
    domain = CharField()

    # 端口 @since v1.2.24
    port = IntegerField(default=443)

    # 别名/备注
    alias = CharField(default="")

    # ip
    # @Deprecated
    ip = CharField(default="")

    # ip信息检查时间 @since 1.2.12
    # @Deprecated
    ip_check_time = DateTimeField(default=None, null=True)

    # 域名信息自动更新 @since v1.2.13
    # @Deprecated
    ip_auto_update = BooleanField(default=True)

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

    # 域名信息自动更新 @since v1.2.13
    domain_auto_update = BooleanField(default=True)

    # 域名过期监测 @since v1.2.24
    domain_expire_monitor = BooleanField(default=True)

    # SSL签发时间
    # @since v1.2.24 变更为：过期时间最短那个证书
    start_time = DateTimeField(default=None, null=True)

    # SSL过期时间
    # @since v1.2.24 变更为：过期时间最短那个证书
    expire_time = DateTimeField(default=None, null=True)

    # SSL过期剩余天数，仅用于排序
    # @since v1.2.24 变更为：过期时间最短那个证书
    expire_days = IntegerField(default=0, null=False)

    # SSL最后检查时间
    # @Deprecated
    check_time = DateTimeField(default=None, null=True)

    # SSL证书信息自动更新 @since v1.2.13
    # @Deprecated
    auto_update = BooleanField(default=True)

    # SSL有效期总天数，仅用于排序
    # @Deprecated
    total_days = IntegerField(default=0, null=False)

    # 连接状态
    # @since v1.2.24 所有ip都连接成功才是成功
    connect_status = BooleanField(default=None, null=True)

    # 通知状态
    notify_status = BooleanField(default=True)

    # 是否监测 @since 1.0.3
    # @Deprecated
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
    def domain_check_time_label(self):
        """
        @since v1.3.1
        :return:
        """
        return datetime_util.time_for_human(self.domain_check_time)

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
    def real_time_ssl_total_days(self):
        """
        实时ssl总天数
        :return:
        @since v1.3.1
        """
        return time_util.get_diff_days(self.start_time, self.expire_time)

    @property
    def real_time_expire_days(self):
        """
        实时ssl过期剩余天数
        expire_days 是更新数据时所计算的时间，有滞后性
        :return:
        """
        if self.expire_time and isinstance(self.expire_time, datetime):
            return (self.expire_time - datetime.now()).days

    # @since v1.3.1
    real_time_ssl_expire_days = real_time_expire_days

    @property
    def real_time_domain_expire_days(self):
        """
        实时域名过期剩余天数
        expire_days 是更新数据时所计算的时间，有滞后性
        @since v1.1.0
        :return:
        """
        if self.domain_expire_time and isinstance(self.domain_expire_time, datetime):
            return (self.domain_expire_time - datetime.now()).days

    @property
    def detail(self):
        if self.detail_raw:
            return json.loads(self.detail_raw)

    @property
    def group(self):
        if self.group_id:
            return GroupModel.get_or_none(GroupModel.id == self.group_id)
