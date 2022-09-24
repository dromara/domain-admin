# -*- coding: utf-8 -*-
from flask import request

from domain_admin.model import GroupModel


def add_group():
    """
    添加
    :return:
    """
    name = request.json.get('name')

    return GroupModel.create(
        name=name
    )


def update_group_by_id():
    """
    更新数据
    :return:
    """
    group_id = request.json.get('id')
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
    group_id = request.json.get('id')

    return GroupModel.delete_by_id(group_id)


def get_group_list():
    """
    获取域名列表
    :return:
    """
    page = request.json.get('page', 1)
    size = request.json.get('size', 10)

    lst = GroupModel.select().order_by(
        GroupModel.update_time.desc()
    ).paginate(page, size)

    total = GroupModel.select().count()

    return {
        'list': lst,
        'total': total
    }


def get_group_by_id():
    """
    获取
    :return:
    """
    group_id = request.json.get('id')

    return GroupModel.get_by_id(group_id)
