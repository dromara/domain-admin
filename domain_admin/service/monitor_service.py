# -*- coding: utf-8 -*-
"""
@File    : monitor_service.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""
from datetime import datetime, timedelta
from functools import wraps

import requests
import six
from peewee import fn

from domain_admin.enums.monitor_status_enum import MonitorStatusEnum
from domain_admin.enums.monitor_type_enum import MonitorTypeEnum
from domain_admin.model.base_model import db
from domain_admin.model.log_monitor_model import LogMonitorModel
from domain_admin.model.monitor_model import MonitorModel
from domain_admin.service import notify_service
from domain_admin.utils import datetime_util


def monitor_log_decorator(func):
    """
    监控任务的日志装饰器
    """

    @wraps(func)
    def wrapper(monitor_row, *args, **kwargs):
        # before
        log_monitor_row = LogMonitorModel.create(
            monitor_id=monitor_row.id,
            monitor_type=monitor_row.monitor_type,
            create_time=datetime.now()
            # create_time=datetime_util.get_datetime_with_microsecond()
        )

        # execute
        result = ''
        error = None

        try:
            result = func(monitor_row, *args, **kwargs)
        except Exception as e:
            error = e

        if error:
            result = six.text_type(error)

        data = {
            'status': MonitorStatusEnum.ERROR if error else MonitorStatusEnum.SUCCESS,
            'result': result or '',
            'update_time': datetime.now()
        }

        LogMonitorModel.update(data).where(
            LogMonitorModel.id == log_monitor_row.id
        ).execute()

        # 继续抛出异常
        if error:
            raise error
        else:
            return result

    return wrapper


def monitor_notify_decorator(func):
    """
    监控任务的日志装饰器
    """

    @wraps(func)
    def wrapper(monitor_row, *args, **kwargs):
        result = None
        error = None

        try:
            result = func(monitor_row, *args, **kwargs)
        except Exception as e:
            error = e

        # 继续抛出异常
        if error:
            notify_service.notify_user_about_monitor_exception(monitor_row, error)
            raise error
        else:
            return result

    return wrapper


def run_monitor_warp(monitor_row):
    error = None

    try:
        run_monitor(monitor_row)
    except Exception as e:
        error = e

    # 计算下次运行时间
    next_run_time = datetime.now() + timedelta(minutes=monitor_row.interval)

    # 同步任务
    MonitorModel.update(
        next_run_time=next_run_time,
        status=MonitorStatusEnum.ERROR if error else MonitorStatusEnum.SUCCESS,
    ).where(
        MonitorModel.id == monitor_row.id
    ).execute()

    if monitor_row.is_active:
        return next_run_time


@monitor_log_decorator
@monitor_notify_decorator
def run_monitor(monitor_row):
    """
    :param monitor_row:
    :return:
    """
    if monitor_row.monitor_type == MonitorTypeEnum.HTTP:
        run_http_monitor(monitor_row)


def run_http_monitor(monitor_row):
    res = requests.request(
        method=monitor_row.content_dict['method'],
        url=monitor_row.content_dict['url'],
        timeout=monitor_row.content_dict['timeout'],
    )

    if not res.ok:
        res.raise_for_status()


@db.connection_context()
def run_monitor_task():
    monitor_rows = MonitorModel.select().where(
        MonitorModel.is_active == True,
        MonitorModel.next_run_time < datetime_util.get_datetime()
    ).order_by(MonitorModel.next_run_time.asc())

    # last_next_run_time = None

    for monitor_row in monitor_rows:
        run_monitor_warp(monitor_row)

    # 返回下次唤醒时间
    monitor_row = MonitorModel.select().where(
        MonitorModel.is_active == True,
    ).order_by(MonitorModel.next_run_time.asc()).first()

    if monitor_row:
        return monitor_row.next_run_time


def load_monitor_log_count(lst):
    monitor_ids = [row['id'] for row in lst]

    # 日志条数
    monitor_groups = LogMonitorModel.select(
        LogMonitorModel.monitor_id,
        fn.COUNT(LogMonitorModel.id).alias('count')
    ).where(
        LogMonitorModel.monitor_id.in_(monitor_ids)
    ).group_by(
        LogMonitorModel.monitor_id
    )

    monitor_groups_map = {
        row.monitor_id: row.count
        for row in monitor_groups
    }

    for row in lst:
        row['log_count'] = monitor_groups_map.get(row['id'])
