# -*- coding: utf-8 -*-
"""
@File    : notify_api.py
@Date    : 2022-10-14
@Author  : Peng Shiyu
"""
import json
import random
import traceback
from datetime import datetime, timedelta

from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.enums.event_enum import EventEnum
from domain_admin.enums.status_enum import StatusEnum
from domain_admin.log import logger
from domain_admin.model.notify_model import NotifyModel
from domain_admin.service import notify_service
from domain_admin.service import work_weixin_service
from domain_admin.utils import datetime_util, time_util


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

    NotifyModel.create(
        user_id=current_user_id,
        event_id=event_id,
        type_id=type_id,
        value_raw=value_raw,
        expire_days=expire_days,
        comment=comment,
        status=StatusEnum.Enabled
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


def get_template_data():
    """
    获取模板参数
    :return:
    """
    current_user_id = g.user_id

    return notify_service.get_template_data(current_user_id)


def handle_test_notify_by_id():
    """
    测试通知配置
    :return:
    """
    current_user_id = g.user_id
    notify_id = request.json['notify_id']
    notify_row = NotifyModel.get_by_id(notify_id)

    days = random.randint(0, 365)
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

    success = 0

    for row in rows:
        try:
            notify_service.notify_user_about_some_event(row)
        except:
            logger.error(traceback.format_exc())

        success = success + 1

    return {
        'success': success
    }


def test_webhook_notify_of_user():
    """
    测试webhook调用
    :return:
    """
    current_user_id = g.user_id

    return notify_service.notify_webhook_of_user(current_user_id)


def test_work_weixin_notify_of_user():
    """
    测试webhook调用
    :return:
    """
    current_user_id = g.user_id
    return work_weixin_service.send_work_weixin_message(current_user_id)
