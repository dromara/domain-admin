# -*- coding: utf-8 -*-
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField

from domain_admin.model.base_model import BaseModel


class VersionModel(BaseModel):
    """记录版本号"""
    id = IntegerField(primary_key=True)

    # 版本号
    version = CharField(unique=True)

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'tb_version'
