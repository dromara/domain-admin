# -*- coding: utf-8 -*-
"""
@File    : group_user_service.py
@Date    : 2023-07-06
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from domain_admin.model.group_model import GroupModel
from domain_admin.model.group_user_model import GroupUserModel


def get_user_group_ids(user_id):
    # 用户创建的组
    group_rows = GroupModel.select().where(
        GroupModel.user_id == user_id
    )

    group_ids = [row.id for row in group_rows]

    # 用户所属的组
    group_user_rows = GroupUserModel.select().where(
        GroupUserModel.user_id == user_id
    )

    user_group_ids = [row.group_id for row in group_user_rows]

    st = set()
    st.update(group_ids)
    st.update(user_group_ids)
    return list(st)


def get_group_user_permission_map(user_id):
    """
    获取用户所在分组的权限关系
    :param user_id: int
    :return: dict
    """
    # 所在分组
    group_user_rows = GroupUserModel.select().where(
        GroupUserModel.user_id == user_id
    )

    # 组员权限
    return {row.group_id: row.has_edit_permission for row in group_user_rows}
