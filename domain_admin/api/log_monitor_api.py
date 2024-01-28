# -*- coding: utf-8 -*-
"""
@File    : log_monitor_api.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""
from flask import g, request
from playhouse.shortcuts import model_to_dict

from domain_admin.model.log_monitor_model import LogMonitorModel


def get_log_monitor_list():
    """
    :return:
    """

    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    monitor_id = request.json.get('monitor_id')

    query = LogMonitorModel.select()
    if monitor_id:
        query = query.where(LogMonitorModel.monitor_id == monitor_id)

    total = query.count()

    lst = []

    if total > 0:
        rows = query.order_by(LogMonitorModel.id.desc()).paginate(page, size)

        lst = [
            model_to_dict(
                model=row,
                extra_attrs=[
                    'create_time_label',
                    'update_time_label',
                    'total_time_label',
                    'total_microsecond_time',
                ]
            ) for row in rows]

    return {
        'list': lst,
        'total': total
    }


def clear_log_monitor():
    """
    :return:
    """
    monitor_id = request.json.get('monitor_id')

    LogMonitorModel.delete().where(
        LogMonitorModel.monitor_id == monitor_id
    ).execute()


def clear_all_log_monitor():
    """
    :return:
    """
    LogMonitorModel.truncate_table()
