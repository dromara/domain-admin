# -*- coding: utf-8 -*-
"""
@File    : notify_api.py
@Date    : 2022-10-14
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import json
import random
import traceback
from datetime import datetime, timedelta

from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.enums.operation_enum import OperationEnum
from domain_admin.enums.status_enum import StatusEnum
from domain_admin.log import logger
from domain_admin.model.notify_model import NotifyModel
from domain_admin.service import notify_service, operation_service
from domain_admin.utils import datetime_util


def get_notify_list_of_user():
    """
    获取用户通知配置
    :return:
    """
    current_user_id = g.user_id
    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    order_prop = request.json.get('order_prop') or 'create_time'
    order_type = request.json.get('order_type') or 'descending'

    query = NotifyModel.select().where(
        NotifyModel.user_id == current_user_id
    )

    total = query.count()

    lst = []

    if total > 0:

        ordering = []

        # order by event_id
        if order_prop == 'event_id':
            if order_type == 'descending':
                ordering.append(NotifyModel.event_id.desc())
            else:
                ordering.append(NotifyModel.event_id.asc())

        # order by type_id
        if order_prop == 'type_id':
            if order_type == 'descending':
                ordering.append(NotifyModel.type_id.desc())
            else:
                ordering.append(NotifyModel.type_id.asc())

        # order by expire_days
        if order_prop == 'expire_days':
            if order_type == 'descending':
                ordering.append(NotifyModel.expire_days.desc())
            else:
                ordering.append(NotifyModel.expire_days.asc())

        # order by status
        if order_prop == 'status':
            if order_type == 'descending':
                ordering.append(NotifyModel.status.desc())
            else:
                ordering.append(NotifyModel.status.asc())

        ordering.append(NotifyModel.id.desc())

        rows = query.order_by(*ordering).paginate(page, size)

        lst = list(map(lambda m: model_to_dict(
            model=m,
            exclude=[NotifyModel.value_raw],
            extra_attrs=[
                'value',
            ]
        ), rows))

    return {
        'list': lst,
        'total': total
    }


@operation_service.operation_log_decorator(
    model=NotifyModel,
    operation_type_id=OperationEnum.CREATE,
    primary_key='id'
)
def add_notify():
    """
    添加用户通知配置
    :return:
    """
    current_user_id = g.user_id

    type_id = request.json['type_id']
    event_id = request.json['event_id']
    value = request.json['value']
    expire_days = request.json['expire_days']
    comment = request.json.get('comment') or ''

    value_raw = json.dumps(value, ensure_ascii=False)

    row = NotifyModel.create(
        user_id=current_user_id,
        event_id=event_id,
        type_id=type_id,
        value_raw=value_raw,
        expire_days=expire_days,
        comment=comment,
        status=StatusEnum.Enabled
    )

    return {'id': row.id}



@operation_service.operation_log_decorator(
    model=NotifyModel,
    operation_type_id=OperationEnum.DELETE,
    primary_key='notify_id'
)
def delete_notify_by_id():
    """
    删除用户通知配置
    :return:
    """
    current_user_id = g.user_id

    notify_id = request.json['notify_id']

    NotifyModel.delete_by_id(notify_id)


def get_notify_by_id():
    """
    获取用户通知配置
    :return:
    """
    current_user_id = g.user_id

    notify_id = request.json['notify_id']

    row = NotifyModel.get_by_id(notify_id)

    return model_to_dict(
        model=row,
        exclude=[NotifyModel.value_raw],
        extra_attrs=[
            'value',
        ])



@operation_service.operation_log_decorator(
    model=NotifyModel,
    operation_type_id=OperationEnum.UPDATE,
    primary_key='notify_id'
)
def update_notify_by_id():
    """
    更新用户通知配置
    :return:
    """
    current_user_id = g.user_id

    notify_id = request.json['notify_id']

    event_id = request.json['event_id']
    value = request.json['value']
    expire_days = request.json['expire_days']
    comment = request.json.get('comment') or ''

    value_raw = json.dumps(value, ensure_ascii=False)

    NotifyModel.update(
        event_id=event_id,
        value_raw=value_raw,
        expire_days=expire_days,
        comment=comment,
    ).where(
        NotifyModel.id == notify_id
    ).execute()


@operation_service.operation_log_decorator(
    model=NotifyModel,
    operation_type_id=OperationEnum.UPDATE,
    primary_key='notify_id'
)
def update_notify_status_by_id():
    """
    更新用户通知配置状态
    :return:
    """
    current_user_id = g.user_id

    notify_id = request.json['notify_id']

    status = request.json['status']

    NotifyModel.update(
        status=status,
    ).where(
        NotifyModel.id == notify_id
    ).execute()


def handle_test_notify_by_id():
    """
    测试通知配置
    :return:
    """
    current_user_id = g.user_id
    notify_id = request.json['notify_id']
    notify_row = NotifyModel.get_by_id(notify_id)

    days = random.randint(1, 365)
    start_date = datetime.now()
    expire_date = start_date + timedelta(days=days)

    lst = [
        {
            'domain': 'www.demo.com',
            'start_date': datetime_util.format_date(start_date),
            'expire_date': datetime_util.format_date(expire_date),
            'expire_days': days
        }
    ]

    return notify_service.notify_user(notify_row, lst)


def handle_notify_by_event_id():
    """
    触发用户的某一类通知操作
    :return:
    """
    current_user_id = g.user_id
    event_id = request.json['event_id']

    rows = NotifyModel.select().where(
        NotifyModel.event_id == event_id,
        NotifyModel.user_id == current_user_id
    )

    total = 0
    success = 0

    for row in rows:
        try:
            notify_service.notify_user_about_some_event(row)
            success = success + 1
        except:
            logger.error(traceback.format_exc())

        total = total + 1

    return {
        'total': total,
        'success': success
    }
