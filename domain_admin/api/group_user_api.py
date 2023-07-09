# -*- coding: utf-8 -*-
"""
group_user_api.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.enums.operation_enum import OperationEnum
from domain_admin.model.group_model import GroupModel
from domain_admin.model.group_user_model import GroupUserModel
from domain_admin.service import group_service, operation_service, common_service


@operation_service.operation_log_decorator(
    model=GroupUserModel,
    operation_type_id=OperationEnum.CREATE,
    primary_key='id'
)
def add_group_user():
    """
    添加
    :return:
    """

    current_user_id = g.user_id

    group_id = request.json['group_id']
    user_id = request.json['user_id']
    has_edit_permission = request.json.get('has_edit_permission', False)

    # 权限校验
    group_service.check_group_permission(group_id, current_user_id)

    row = GroupUserModel.create(
        group_id=group_id,
        user_id=user_id,
        has_edit_permission=has_edit_permission
    )

    return {'id': row.id}


@operation_service.operation_log_decorator(
    model=GroupUserModel,
    operation_type_id=OperationEnum.UPDATE,
    primary_key='group_user_id'
)
def update_group_user_by_id():
    """
    更新数据
    :return:
    """

    current_user_id = g.user_id

    group_user_id = request.json['group_user_id']
    has_edit_permission = request.json.get('has_edit_permission', False)

    group_user_row = GroupUserModel.get_by_id(group_user_id)

    group_service.check_group_permission(group_user_row.group_id, current_user_id)

    GroupUserModel.update(
        has_edit_permission=has_edit_permission,
    ).where(
        GroupUserModel.id == group_user_id
    ).execute()


@operation_service.operation_log_decorator(
    model=GroupUserModel,
    operation_type_id=OperationEnum.DELETE,
    primary_key='group_user_id'
)
def delete_group_user_by_id():
    """
    删除
    :return:
    """
    current_user_id = g.user_id

    group_user_id = request.json['group_user_id']

    group_user_row = GroupUserModel.get_by_id(group_user_id)

    group_service.check_group_permission(group_user_row.group_id, current_user_id)

    GroupUserModel.delete().where(
        GroupUserModel.id == group_user_id,
    ).execute()


@operation_service.operation_log_decorator(
    model=GroupUserModel,
    operation_type_id=OperationEnum.BATCH_DELETE,
    primary_key='group_user_ids'
)
def delete_group_user_by_ids():
    """
    批量删除
    :return:
    """
    current_user_id = g.user_id

    group_user_ids = request.json['group_user_ids']

    group_user_rows = GroupUserModel.select().where(
        GroupUserModel.id.in_(group_user_ids)
    )

    for group_user_row in group_user_rows:
        group_service.check_group_permission(group_user_row.group_id, current_user_id)

    GroupUserModel.delete().where(
        GroupUserModel.id.in_(group_user_ids),
    ).execute()


def get_group_user_list():
    """
    获取列表
    :return:
    """
    current_user_id = g.user_id
    group_id = request.json.get('group_id')

    # 分组列表数据
    query = GroupUserModel.select().where(
        GroupUserModel.group_id == group_id
    )

    total = query.count()

    rows = query.order_by(
        GroupUserModel.create_time.asc(),
        GroupUserModel.id.asc()
    )

    lst = [model_to_dict(row) for row in rows]

    # 添加leader
    group_row = GroupModel.get_by_id(group_id)

    leader = GroupUserModel()
    leader.group_id = group_id
    leader.user_id = group_row.user_id
    leader.has_edit_permission = True

    lst.insert(0, model_to_dict(leader))

    common_service.load_user_name(lst)

    for row in lst:
        # add leader
        if row['user_id'] == group_row.user_id:
            row['is_leader'] = True
        else:
            row['is_leader'] = False

    return {
        'list': lst,
        'total': len(lst),
    }


def get_group_user_by_id():
    """
    获取
    :return:
    """
    current_user_id = g.user_id

    group_id = request.json['group_id']

    group_service.check_group_permission(group_id, current_user_id)

    return GroupUserModel.get_by_id(group_id)
