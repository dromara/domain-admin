# -*- coding: utf-8 -*-
"""
@File    : monitor_service.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""
import json
from datetime import datetime, timedelta
from functools import wraps

import requests
import six
from peewee import fn, chunked

from domain_admin.config import USER_AGENT
from domain_admin.enums.monitor_status_enum import MonitorStatusEnum
from domain_admin.enums.monitor_type_enum import MonitorTypeEnum
from domain_admin.model import monitor_model
from domain_admin.model.base_model import db
from domain_admin.model.log_monitor_model import LogMonitorModel
from domain_admin.model.monitor_model import MonitorModel
from domain_admin.service import notify_service, file_service, async_task_service
from domain_admin.service.scheduler_service import scheduler_main
from domain_admin.utils import datetime_util, file_util


def monitor_log_decorator(func):
    """
    监控任务的日志装饰器
    """

    @wraps(func)
    def wrapper(monitor_row, *args, **kwargs):

        # execute
        result = ''
        error = None

        start_time = datetime.now()

        try:
            result = func(monitor_row, *args, **kwargs)
        except Exception as e:
            error = e

        if error:
            result = six.text_type(error)

        # 记录日志
        LogMonitorModel.create(
            monitor_id=monitor_row.id,
            monitor_type=monitor_row.monitor_type,
            create_time=start_time,
            update_time=datetime.now(),
            result=result or '',
            status=MonitorStatusEnum.ERROR if error else MonitorStatusEnum.SUCCESS,
        )

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
            handle_monitor_exception(monitor_row, error)
            raise error
        else:
            return result

    return wrapper


def handle_monitor_exception(monitor_row, error):
    if monitor_row.allow_error_count > 0:
        # 检查连续失败次数是否大于最大允许失败次数，增加容错
        rows = LogMonitorModel.select().where(
            LogMonitorModel.monitor_id == monitor_row.id,
        ).order_by(
            LogMonitorModel.id.desc()
        ).limit(
            monitor_row.allow_error_count + 1
        )

        error_count = len([row for row in rows if row.status == MonitorStatusEnum.ERROR])

        if error_count <= monitor_row.allow_error_count:
            return

    # 发送异常通知
    notify_service.notify_user_about_monitor_exception(monitor_row, error)


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
        version=MonitorModel.version + 1
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
        run_http_monitor(
            method=monitor_row.content_dict['method'],
            url=monitor_row.content_dict['url'],
            timeout=int(monitor_row.content_dict['timeout'])
        )


def run_http_monitor(url, method='GET', timeout=3):
    res = requests.request(
        method=method,
        url=url,
        timeout=timeout,
        headers={
            "User-Agent": USER_AGENT
        }
    )

    if not res.ok:
        res.raise_for_status()

    return res.text


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


def get_monitor_list_query(**params):
    query = MonitorModel.select()

    status = params.get("status")
    if isinstance(status, int):
        query = query.where(MonitorModel.status == status)

    keyword = params.get('keyword')
    if keyword:
        query = query.where(MonitorModel.title.contains(keyword))

    user_id = params.get('user_id')
    if user_id:
        query = query.where(MonitorModel.user_id == user_id)

    return query


def export_monitor_to_file(rows, ext):
    """
    导出域名到文件
    :param rows:
    :return:
    """

    filename = datetime.now().strftime("monitor_%Y%m%d%H%M%S") + '.' + ext
    temp_filename = file_service.resolve_temp_file(filename)

    lst = file_util.convert_to_export(rows, monitor_model.FIELD_MAPPING)

    file_util.write_data_to_file(temp_filename, lst)

    return filename


def import_monitor_from_file(filename, user_id):
    rows = file_util.read_data_from_file(filename)

    lst = file_util.convert_to_import(rows, monitor_model.FIELD_MAPPING)
    print(lst)

    lst = [
        {
            'title': item['title'],
            'monitor_type': MonitorTypeEnum.HTTP,
            'interval': int(item.get('interval') or '60'),
            'content': json.dumps({
                'url': item['http_url'],
                'method': 'GET',
                'timeout': int(item.get('http_timeout') or '3'),
            }),
            'user_id': user_id,
        } for item in lst
    ]

    # fix: peewee.OperationalError: too many SQL variables
    # https://github.com/mouday/domain-admin/issues/63
    for batch in chunked(lst, 500):
        MonitorModel.insert_many(batch).on_conflict_ignore().execute()
