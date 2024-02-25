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

from domain_admin.enums.operation_enum import OperationEnum
from domain_admin.model.log_monitor_model import LogMonitorModel
from domain_admin.model.monitor_model import MonitorModel
from domain_admin.service import monitor_service, file_service, async_task_service, operation_service
from domain_admin.service.scheduler_service import scheduler_main


def add_monitor():
    """

    :return:
    """
    current_user_id = g.user_id
    title = request.json['title']
    monitor_type = request.json['monitor_type']
    allow_error_count = request.json.get('allow_error_count') or 0
    content = request.json['content']
    interval = request.json['interval']

    monitor_row = MonitorModel.create(
        user_id=current_user_id,
        title=title,
        allow_error_count=allow_error_count,
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
    allow_error_count = request.json.get('allow_error_count') or 0

    MonitorModel.update(
        title=title,
        content=json.dumps(content),
        interval=interval,
        allow_error_count=allow_error_count,
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

    if is_active:
        next_run_time = datetime.now()
    else:
        next_run_time = None

    MonitorModel.update(
        is_active=is_active,
        next_run_time=next_run_time
    ).where(
        MonitorModel.id == monitor_id
    ).execute()

    if is_active:
        scheduler_main.run_one_monitor_task(MonitorModel.get_by_id(monitor_id))


def remove_monitor_by_id():
    """

    :return:
    """
    monitor_id = request.json['monitor_id']

    MonitorModel.delete_by_id(monitor_id)



@operation_service.operation_log_decorator(
    model=MonitorModel,
    operation_type_id=OperationEnum.BATCH_DELETE,
    primary_key='monitor_ids'
)
def delete_monitor_by_ids():
    """
    批量删除
    @since v1.6.12
    :return:
    """
    current_user_id = g.user_id

    monitor_ids = request.json['monitor_ids']

    MonitorModel.delete().where(
        MonitorModel.id.in_(monitor_ids),
        MonitorModel.user_id == current_user_id
    ).execute()


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
    status = request.json.get('status')

    query = MonitorModel.select().where(
        MonitorModel.user_id == current_user_id
    )

    if keyword:
        query = query.where(MonitorModel.title.contains(keyword))

    if isinstance(status, int):
        query = query.where(MonitorModel.status == status)

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


def export_monitor_file():
    """
    导出监控文件
    csv格式
    :return:
    """
    current_user_id = g.user_id

    keyword = request.json.get('keyword')
    status = request.json.get('status')
    ext = request.json.get('ext', 'csv')

    order_prop = request.json.get('order_prop') or 'create_time'
    order_type = request.json.get('order_type') or 'desc'

    params = {
        'keyword': keyword,
        'status': status,
        'user_id': current_user_id,
    }

    query = monitor_service.get_monitor_list_query(**params)

    ordering = [
        SQL(f"`{order_prop}` {order_type}"),
        MonitorModel.id.desc()
    ]

    rows = query.order_by(*ordering)

    lst = [row.to_dict() for row in rows]

    filename = monitor_service.export_monitor_to_file(rows=lst, ext=ext)

    return {
        'name': filename,
        'url': file_service.resolve_temp_url(filename)
    }


def import_monitor_from_file():
    """
    从文件导入域名
    支持 xlsx 和 csv格式
    :return:
    """
    current_user_id = g.user_id

    update_file = request.files.get('file')

    filename = file_service.save_temp_file(update_file)

    # 导入数据
    monitor_service.import_monitor_from_file(filename, current_user_id)

    # 异步查询
    run_init_monitor_task_async(user_id=current_user_id)


@async_task_service.async_task_decorator("更新监控信息")
def run_init_monitor_task_async(user_id):
    rows = MonitorModel.select().where(
        MonitorModel.user_id == user_id,
        MonitorModel.version == 0
    )

    for row in rows:
        scheduler_main.run_one_monitor_task(row)
