# -*- coding: utf-8 -*-
"""
@File    : group_user_service.py
@Date    : 2023-07-06
"""
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

    return list(set(*group_ids, *user_group_ids))
