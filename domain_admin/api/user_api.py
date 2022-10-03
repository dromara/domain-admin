# -*- coding: utf-8 -*-
import json

from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.model.user_model import UserModel
from domain_admin.utils import datetime_util


def get_user_info():
    """
    获取当前用户信息
    :return:
    """
    current_user_id = g.user_id

    row = UserModel.get_by_id(current_user_id)

    return model_to_dict(
        model=row,
        exclude=[UserModel.password],
        extra_attrs=['email_list']
    )


def update_user_info():
    """
    更新当前用户信息
    :return:
    """
    current_user_id = g.user_id

    avatar_url = request.json.get('avatar_url')
    before_expire_days = request.json.get('before_expire_days')
    email_list = request.json.get('email_list')

    UserModel.update({
        'avatar_url': avatar_url,
        'before_expire_days': before_expire_days,
        'email_list_raw': json.dumps(email_list, ensure_ascii=False),
        'update_time': datetime_util.get_datetime()
    }).where(
        UserModel.id == current_user_id
    ).execute()
