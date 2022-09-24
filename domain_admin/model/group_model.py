# -*- coding: utf-8 -*-
from datetime import datetime

from domain_admin.model.base_model import BaseModel
from peewee import CharField, IntegerField, DateTimeField, BooleanField


class GroupModel(BaseModel):
    """分组"""
    id = IntegerField(primary_key=True)

    # 名称
    name = CharField()

    # 创建时间
    create_time = DateTimeField(default=datetime.now)

    # 更新时间
    update_time = DateTimeField(default=datetime.now)
