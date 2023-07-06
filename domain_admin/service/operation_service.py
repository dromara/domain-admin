# -*- coding: utf-8 -*-
"""
@File    : operation_service.py
@Date    : 2023-07-04
"""
from functools import wraps
from typing import Dict

from flask import g, request

from domain_admin.enums.operation_enum import OperationEnum
from domain_admin.model.base_model import BaseModel
from domain_admin.model.log_operation_model import LogOperationModel
from domain_admin.utils import json_util


def add_operation_log(user_id: int, table: str, type_id: int, before: Dict, after: Dict):
    """
    添加操作日志
    table = model._meta.table_name
    :param type_id:
    :param after:
    :param user_id:
    :param table:
    :param before:
    :return:
    """

    LogOperationModel.create(
        user_id=user_id,
        table=table,
        type_id=type_id,
        before=json_util.json_encode(before),
        after=json_util.json_encode(after)
    )


def operation_log_decorator(
        model: BaseModel,
        operation_type_id: int,
        primary_key: str = 'id'
):
    """
    用于添加操作日志装饰器
    :param primary_key: 主键id key
    :param model: Model
    :param operation_type_id: 操作类型id
    :return:
    """

    def outer_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            before = None
            after = None

            # before
            if OperationEnum.CREATE == operation_type_id:
                before = None

            elif OperationEnum.UPDATE == operation_type_id:
                before = model.get_by_id(request.json[primary_key])

            elif OperationEnum.DELETE == operation_type_id:
                before = model.get_by_id(request.json[primary_key])

            elif OperationEnum.BATCH_DELETE == operation_type_id:
                before = list(model.select().where(
                    model.id.in_(request.json[primary_key])
                ))

            # execute
            ret = func(*args, **kwargs)

            # after
            if OperationEnum.CREATE == operation_type_id:
                after = model.get_by_id(ret[primary_key])

            if OperationEnum.UPDATE == operation_type_id:
                after = model.get_by_id(request.json[primary_key])

            if OperationEnum.DELETE == operation_type_id:
                after = None

            current_user_id = g.user_id

            # 写入log
            add_operation_log(
                user_id=current_user_id,
                table=model._meta.table_name,
                type_id=operation_type_id,
                before=before,
                after=after
            )

            return ret

        return wrapper

    return outer_wrapper
