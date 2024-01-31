# -*- coding: utf-8 -*-
"""
@File    : monitor_api.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""
import json
from datetime import datetime, timedelta

from flask import request, g
from peewee import SQL, fn
from playhouse.shortcuts import model_to_dict

from domain_admin.model.log_monitor_model import LogMonitorModel
from domain_admin.model.monitor_model import MonitorModel
from domain_admin.service import monitor_service
from domain_admin.service.scheduler_service import scheduler_main


def add_monitor():
    """

    :return:
    """
    current_user_id = g.user_id
    title = request.json['title']
    monitor_type = request.json['monitor_type']
    content = request.json['content']
    interval = request.json['interval']

    monitor_row = MonitorModel.create(
        user_id=current_user_id,
        title=title,
        monitor_type=monitor_type,
        content=json.dumps(content),
        interval=interval
    )

    scheduler_main.run_one_monitor_task(MonitorModel.get_by_id(monitor_row.id))


def update_monitor_by_id():
    """

    :return:
    """
    current_user_id = g.user_id

    monitor_id = request.json['monitor_id']
    title = request.json['title']
    content = request.json['content']
    interval = request.json['interval']

    MonitorModel.update(
        title=title,
        content=json.dumps(content),
        interval=interval
    ).where(
        MonitorModel.id == monitor_id
    ).execute()

    scheduler_main.run_one_monitor_task(MonitorModel.get_by_id(monitor_id))


def update_monitor_active():
    """
    :return:
    """
    monitor_id = request.json['monitor_id']
    is_active = request.json['is_active']

    MonitorModel.update(
        is_active=is_active,
        next_run_time=None
    ).where(
        MonitorModel.id == monitor_id
    ).execute()


def remove_monitor_by_id():
    """

    :return:
    """
    monitor_id = request.json['monitor_id']

    MonitorModel.delete_by_id(monitor_id)


def get_monitor_by_id():
    """

    :return:
    """
    monitor_id = request.json['monitor_id']

    monitor_row = MonitorModel.get_by_id(monitor_id)

    return monitor_row.to_dict()


def get_monitor_list():
    """

    :return:
    """
    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    order_prop = request.json.get('order_prop') or 'create_time'
    order_type = request.json.get('order_type') or 'desc'
    keyword = request.json.get('keyword')

    query = MonitorModel.select().where(
        MonitorModel.user_id == current_user_id
    )

    if keyword:
        query = query.where(MonitorModel.title.contains(keyword))

    total = query.count()

    lst = []

    if total > 0:
        ordering = [
            SQL(f"`{order_prop}` {order_type}"),
            MonitorModel.id.desc()
        ]

        rows = query.order_by(*ordering).paginate(page, size)

        lst = [row.to_dict() for row in rows]

        monitor_service.load_monitor_log_count(lst)

    return {
        'list': lst,
        'total': total
    }
