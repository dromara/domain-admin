# -*- coding: utf-8 -*-
from flask import request, g

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

    group_service.check_group_permission(group_id, current_user_id)

    name = request.json.get('name')

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

    current_user_id = g.user_id

    lst = GroupModel.select().where(
        GroupModel.user_id == current_user_id
    ).order_by(
        GroupModel.create_time.asc(),
        GroupModel.id.asc()
    )

    total = GroupModel.select().where(
        GroupModel.user_id == current_user_id
    ).count()

    return {
        'list': lst,
        'total': total
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
