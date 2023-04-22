# -*- coding: utf-8 -*-
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField

from domain_admin.model.base_model import BaseModel


class CacheDomainInfoModel(BaseModel):
    """
    域名信息缓存表
    @since 1.2.12
    """
    id = IntegerField(primary_key=True)

    # 域名
    domain = CharField(unique=True)

    # 域名注册时间
    domain_start_time = DateTimeField(default=None, null=True)

    # 域名过期时间
    domain_expire_time = DateTimeField(default=None, null=True)

    # 缓存过期时间
    expire_time = DateTimeField(default=None, null=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'cache_domain_info'

    @property
    def is_expired(self) -> [bool, None]:
        """
        过期时间
        :return:
        """
        if self.expire_time:
            return (self.expire_time - datetime.now()).seconds <= 0
        else:
            return None

    @property
    def domain_expire_days(self) -> [int, None]:
        """域名过期天数"""
        if self.domain_expire_time:
            return (self.domain_expire_time - datetime.now()).days
        else:
            return None
