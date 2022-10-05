# -*- coding: utf-8 -*-
"""
user_api.py
"""

import json

from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.model.user_model import UserModel
from domain_admin.utils import datetime_util, bcrypt_util
from domain_admin.utils.flask_ext.app_exception import AppException


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


def update_user_password():
    """
    更新用户密码
    :return:
    """
    current_user_id = g.user_id

    password = request.json.get('password')
    new_password = request.json.get('new_password')

    user_row = UserModel.get_by_id(current_user_id)

    if not bcrypt_util.check_password(password, user_row.password):
        raise AppException('旧密码不正确')

    UserModel.update(
        {
            'password': bcrypt_util.encode_password(new_password),
        }
    ).where(
        UserModel.id == current_user_id
    ).execute()


def get_user_list():
    """
    获取当前用户信息
    :return:
    """
    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    keyword = request.json.get('keyword')

    query = UserModel.select()

    if keyword:
        query = query.where(UserModel.username.contains(keyword))

    total = query.count()
    lst = query.order_by(
        UserModel.create_time.desc(),
        UserModel.id.desc(),
    ).paginate(page, size)

    lst = list(map(lambda m: model_to_dict(
        model=m,
        extra_attrs=[
            'email_list',
        ]
    ), lst))

    return {
        'list': lst,
        'total': total
    }


def add_user():
    """
    获取当前用户信息
    :return:
    """
    username = request.json.get('username')
    password = request.json.get('password')

    row = UserModel.select().where(
        UserModel.username == username
    ).get_or_none()

    if row:
        raise AppException('用户已存在')

    UserModel.create(
        username=username,
        password=bcrypt_util.encode_password(password)
    )


def update_user_status():
    """
    获取当前用户信息
    :return:
    """
    user_id = request.json.get('user_id')
    status = request.json.get('status')

    UserModel.update({
        'status': status
    }).where(
        UserModel.id == user_id
    ).execute()


def delete_user():
    """
    获取当前用户信息
    :return:
    """
    user_id = request.json.get('user_id')

    UserModel.delete_by_id(user_id)
