# -*- coding: utf-8 -*-
"""
log_scheduler_api.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.model.log_scheduler_model import LogSchedulerModel


def get_log_scheduler_list():
    """
    获取调度日志列表
    :return:
    """
    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)

    query = LogSchedulerModel.select()

    total = query.count()

    lst = []
    if total > 0:
        rows = query.order_by(
            LogSchedulerModel.create_time.desc(),
            LogSchedulerModel.id.desc(),
        ).paginate(page, size)

        lst = list(map(lambda m: model_to_dict(
            model=m,
            extra_attrs=[
                'total_time',
                'total_time_label',
            ]
        ), rows))

    return {
        'list': lst,
        'total': total
    }


def clear_log_scheduler_list():
    """
    清空日志
    :return:
    """
    LogSchedulerModel.truncate_table()
