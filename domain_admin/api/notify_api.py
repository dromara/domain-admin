# -*- coding: utf-8 -*-
"""
@File    : notify_api.py
@Date    : 2022-10-14
@Author  : Peng Shiyu
"""
import json

from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.model.notify_model import NotifyModel
from domain_admin.service import notify_service


def get_notify_of_user():
    """
    获取用户通知配置
    :return:
    """
    current_user_id = g.user_id

    type_id = request.json['type_id']

    row = NotifyModel.get_or_none(
        NotifyModel.user_id == current_user_id,
        NotifyModel.type_id == type_id
    )

    if row:
        return model_to_dict(
            model=row,
            exclude=[NotifyModel.value_raw],
            extra_attrs=[
                'value',
            ]
        )


def update_notify_of_user():
    """
    更新用户通知配置
    :return:
    """
    current_user_id = g.user_id

    type_id = request.json['type_id']
    value = request.json['value']

    row = NotifyModel.get_or_none(
        NotifyModel.user_id == current_user_id,
        NotifyModel.type_id == type_id
    )

    value_raw = json.dumps(value, ensure_ascii=False)

    if row:
        NotifyModel.update(
            value_raw=value_raw
        ).where(
            NotifyModel.id == row.id
        ).execute()
    else:
        NotifyModel.create(
            user_id=current_user_id,
            type_id=type_id,
            value_raw=value_raw
        )

def test_webhook_notify_of_user():
    """
    测试webhook调用
    :return:
    """
    current_user_id = g.user_id

    return notify_service.notify_webhook_of_user(current_user_id)