# -*- coding: utf-8 -*-
from flask import request, g
from peewee import fn
from playhouse.shortcuts import model_to_dict

from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.service import group_service


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


def delete_group_by_id():
    """
    删除
    :return:
    """
    current_user_id = g.user_id

    group_id = request.json['id']

    group_service.check_group_permission(group_id, current_user_id)

    GroupModel.delete_by_id(group_id)


def get_group_list():
    """
    获取域名列表
    :return:
    """
    # page = request.json.get('page', 1)
    # size = request.json.get('size', 10)
    keyword = request.json.get('keyword')

    current_user_id = g.user_id

    # 分组列表数据
    query = GroupModel.select().where(
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

    # 域名分组统计
    domain_groups = DomainModel.select(
        DomainModel.group_id,
        fn.COUNT().alias('count')
    ).group_by(DomainModel.group_id)

    domain_groups_map = {
        row.group_id: row.count
        for row in domain_groups
    }

    lst = []
    for row in rows:
        row_dict = model_to_dict(row)
        row_dict['domain_count'] = domain_groups_map.get(row.id, 0)
        lst.append(row_dict)

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
