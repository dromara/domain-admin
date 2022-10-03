# -*- coding: utf-8 -*-
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
