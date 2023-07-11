# -*- coding: utf-8 -*-
"""
group_service.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from __future__ import print_function, unicode_literals, absolute_import, division

from peewee import chunked

from domain_admin.model.group_model import GroupModel
from domain_admin.utils.flask_ext.app_exception import ForbiddenAppException


def check_group_permission(group_id, user_id):
    """
    权限检查
    :param group_id:
    :param user_id:
    :return:
    """

    group_row = GroupModel.get_by_id(group_id)
    if group_row.user_id != user_id:
        raise ForbiddenAppException()


def get_or_create_group_map(lst, user_id):
    """
    获取分组名和分组id映射关系，如果不存在则导入
    :param lst: List[str] 分组列表
    :param user_id: int 用户id
    :return:
    """
    # 导入分组
    group_name_list = list(set(name for name in lst if name and name.strip()))

    group_map = get_group_map(group_name_list, user_id)

    # 比较
    if len(group_name_list) > len(group_map):
        new_group_name_list = [
            {
                'name': group_name,
                'user_id': user_id,
            } for group_name in group_name_list
            if group_name not in group_map
        ]

        # 批量写入
        if new_group_name_list:
            for batch in chunked(new_group_name_list, 500):
                GroupModel.insert_many(batch).execute()

        group_map = get_group_map(group_name_list, user_id)

    return group_map


def get_group_map(lst, user_id):
    """
    获取分组映射
    :param lst:  List[str]
    :param user_id: int
    :return:
    """
    group_rows = GroupModel.select().where(
        GroupModel.name.in_(lst),
        GroupModel.user_id == user_id
    )

    return {
        group_row.name: group_row.id
        for group_row in group_rows
    }


def load_group_name(lst):
    """
    加载分类名
    :param lst:
    :return: list with group_name
    """
    group_ids = [row['group_id'] for row in lst]

    # 主机数量
    group_rows = GroupModel.select().where(
        GroupModel.id.in_(group_ids)
    )

    group_map = {
        str(group_row.id): group_row.name
        for group_row in group_rows
    }

    for row in lst:
        row['group_name'] = group_map.get(str(row['group_id']), '')

    return lst


def get_group_name_by_id(group_id):
    """
    获取分组名称
    :param group_id:
    :return:
    """
    row = GroupModel.get_or_none(group_id)
    if row:
        return row.name
