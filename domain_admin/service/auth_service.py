# -*- coding: utf-8 -*-
"""
auth_service.py
"""

from domain_admin.model.user_model import UserModel
from domain_admin.service import token_service
from domain_admin.utils import bcrypt_util
from domain_admin.utils.flask_ext.app_exception import AppException


def login(username, password):
    """
    用户登录
    :param username:
    :param password:
    :return:
    """
    user_row = UserModel.select().where(
        UserModel.username == username
    ).get_or_none()

    if not user_row:
        raise AppException('用户名或密码错误')

    if not bcrypt_util.check_password(password, user_row.password):
        raise AppException('用户名或密码错误')

    if not user_row.status:
        raise AppException('账号不可用')

    return token_service.encode_token({
        'user_id': user_row.id
    })


def register(username, password, password_repeat):
    """
    用户注册
    :param username:
    :param password:
    :param password_repeat:
    :return:
    """
    user_row = UserModel.select().where(
        UserModel.username == username
    ).get_or_none()

    if user_row:
        raise AppException('用户已存在')

    if password != password_repeat:
        raise AppException('密码不一致')

    return UserModel.create(
        username=username,
        password=bcrypt_util.encode_password(password)
    )
