# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
from operator import itemgetter

from flask import request, g
from peewee import fn
from playhouse.shortcuts import model_to_dict

from domain_admin.enums.operation_enum import OperationEnum
from domain_admin.enums.role_enum import RoleEnum
from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.model.group_user_model import GroupUserModel
from domain_admin.service import group_service, operation_service, group_user_service


@operation_service.operation_log_decorator(
    model=GroupModel,
    operation_type_id=OperationEnum.CREATE,
    primary_key='id'
)
def add_group():
    """
    添加
    :return:
    """

    current_user_id = g.user_id

    name = request.json['name']

    row = GroupModel.create(
        name=name,
        user_id=current_user_id
    )

    return {'id': row.id}


@operation_service.operation_log_decorator(
    model=GroupModel,
    operation_type_id=OperationEnum.UPDATE,
    primary_key='id'
)
def update_group_by_id():
    """
    更新数据
    :return:
    """

    current_user_id = g.user_id

    group_id = request.json['id']
    name = request.json.get('name')

    group_service.check_group_permission(group_id, current_user_id)

    GroupModel.update(
        name=name,
    ).where(
        GroupModel.id == group_id
    ).execute()


@operation_service.operation_log_decorator(
    model=GroupModel,
    operation_type_id=OperationEnum.DELETE,
    primary_key='id'
)
def delete_group_by_id():
    """
    删除
    :return:
    """
    current_user_id = g.user_id

    group_id = request.json['id']

    GroupModel.delete().where(
        GroupModel.id == group_id,
        GroupModel.user_id == current_user_id
    ).execute()

    # 重置已分类的证书 和 域名
    DomainModel.update(
        group_id=0
    ).where(
        DomainModel.group_id == group_id
    ).execute()

    DomainInfoModel.update(
        group_id=0
    ).where(
        DomainInfoModel.group_id == group_id
    ).execute()

    GroupUserModel.delete().where(
        GroupUserModel.group_id == group_id
    ).execute()


@operation_service.operation_log_decorator(
    model=GroupModel,
    operation_type_id=OperationEnum.BATCH_DELETE,
    primary_key='group_ids'
)
def delete_group_by_ids():
    """
    批量删除
    :return:
    """
    current_user_id = g.user_id

    group_ids = request.json['group_ids']

    GroupModel.delete().where(
        GroupModel.id.in_(group_ids),
        GroupModel.user_id == current_user_id
    ).execute()

    # 重置已分类的证书 和 域名
    DomainModel.update(
        group_id=0
    ).where(
        DomainModel.group_id.in_(group_ids)
    ).execute()

    DomainInfoModel.update(
        group_id=0
    ).where(
        DomainInfoModel.group_id.in_(group_ids)
    ).execute()

    GroupUserModel.delete().where(
        GroupUserModel.group_id.in_(group_ids)
    ).execute()


def get_group_list():
    """
    获取域名列表
    :return:
    """
    # page = request.json.get('page', 1)
    # size = request.json.get('size', 10)
    keyword = request.json.get('keyword')
    role = request.json.get('role')

    current_user_id = g.user_id

    # 分组列表数据
    query = GroupModel.select()

    # 所在分组
    group_user_list = list(GroupUserModel.select().where(
        GroupUserModel.user_id == current_user_id
    ))

    user_group_ids = [row.group_id for row in group_user_list]
    group_user_map = {row.group_id: row.has_edit_permission for row in group_user_list}

    if role == RoleEnum.ADMIN:
        pass

    elif user_group_ids:
        query = query.where(
            (GroupModel.user_id == current_user_id)
            | (GroupModel.id.in_(user_group_ids))
        )
    else:
        query = query.where(
            GroupModel.user_id == current_user_id
        )

    if keyword:
        query = query.where(GroupModel.name.contains(keyword))

    total = query.count()

    # bugfix: 分组不需要分页
    rows = query.order_by(
        GroupModel.create_time.asc(),
        GroupModel.id.asc()
    )

    rows = list(rows)

    # 证书分组统计
    cert_groups = DomainModel.select(
        DomainModel.group_id,
        fn.COUNT(DomainModel.id).alias('count')
    ).group_by(DomainModel.group_id)

    cert_groups_map = {
        row.group_id: row.count
        for row in cert_groups
    }

    # 域名分组统计
    domain_groups = DomainInfoModel.select(
        DomainInfoModel.group_id,
        fn.COUNT(DomainInfoModel.id).alias('count')
    ).group_by(DomainInfoModel.group_id)

    domain_groups_map = {
        row.group_id: row.count
        for row in domain_groups
    }

    # 成员分组统计
    group_ids = [row.id for row in rows]

    domain_groups = GroupUserModel.select(
        GroupUserModel.group_id,
        fn.COUNT(GroupUserModel.id).alias('count')
    ).where(
        GroupUserModel.group_id.in_(group_ids)
    ).group_by(GroupUserModel.group_id)

    group_user_groups_map = {
        row.group_id: row.count
        for row in domain_groups
    }

    lst = []
    for row in rows:
        row_dict = model_to_dict(row)
        row_dict['cert_count'] = cert_groups_map.get(row.id, 0)
        row_dict['domain_count'] = domain_groups_map.get(row.id, 0)
        row_dict['group_user_count'] = group_user_groups_map.get(row.id, 0) + 1

        # 组权限
        if role == RoleEnum.ADMIN:
            has_edit_permission = True

        elif row.user_id == current_user_id:
            has_edit_permission = True
        else:
            has_edit_permission = group_user_map.get(row.id, False)

        row_dict['has_edit_permission'] = has_edit_permission
        row_dict['is_leader'] = row.user_id == current_user_id

        lst.append(row_dict)

    lst.sort(key=itemgetter('is_leader', 'has_edit_permission'), reverse=True)

    return {
        'list': lst,
        'total': total,
    }


def get_group_by_id():
    """
    获取
    :return:
    """
    current_user_id = g.user_id

    group_id = request.json['id']

    group_service.check_group_permission(group_id, current_user_id)

    return GroupModel.get_by_id(group_id)
