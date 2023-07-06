# -*- coding: utf-8 -*-
"""
@File    : common_service.py
@Date    : 2023-07-04
"""
from typing import List

from domain_admin.model.base_model import BaseModel
from domain_admin.model.user_model import UserModel


def load_user_name(lst: List[BaseModel]):
    """
    追加用户名字段: user_name
    :param lst:
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
