# -*- coding: utf-8 -*-
"""
log_async_task_api.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.model.log_async_task_model import AsyncTaskModel
from domain_admin.model.log_operation_model import LogOperationModel
from domain_admin.service import common_service


def get_async_task_log_list():
    """
    获取操作日志列表
    :return:
    """
    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)

    query = AsyncTaskModel.select()

    total = query.count()

    lst = []

    if total > 0:
        rows = query.order_by(
            AsyncTaskModel.create_time.desc(),
            AsyncTaskModel.id.desc(),
        ).paginate(page, size)

        lst = [model_to_dict(model=row, extra_attrs=[
            'total_time',
            'total_time_label',
            'create_time_label',
        ]) for row in rows]

        common_service.load_user_name(lst)

    return {
        'list': lst,
        'total': total
    }


def clear_async_task_log_list():
    """
    清空日志
    :return:
    """
    AsyncTaskModel.truncate_table()
