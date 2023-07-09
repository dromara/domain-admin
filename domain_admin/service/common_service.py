# -*- coding: utf-8 -*-
"""
@File    : common_service.py
@Date    : 2023-07-04
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.model.user_model import UserModel


def load_user_name(lst):
    """
    追加用户名字段: user_name
    :param lst: List[BaseModel]
    :return:
    """
    user_ids = [row['user_id'] for row in lst]

    # 主机数量
    user_rows = UserModel.select().where(
        UserModel.id.in_(user_ids)
    )

    user_map = {
        str(user_row.id): user_row.username
        for user_row in user_rows
    }

    for row in lst:
        row['user_name'] = user_map.get(str(row['user_id']), '')

    return lst
