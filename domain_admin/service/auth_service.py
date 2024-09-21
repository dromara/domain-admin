# -*- coding: utf-8 -*-
"""
auth_service.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from functools import wraps

from flask import g

from domain_admin.enums.role_enum import RoleEnum, ROLE_PERMISSION
from domain_admin.enums.status_enum import StatusEnum
from domain_admin.model.user_model import UserModel
from domain_admin.service import token_service, notify_service, async_task_service
from domain_admin.utils import bcrypt_util, cache_util, validate_util, secret_util
from domain_admin.utils.flask_ext.app_exception import AppException


def login(username, password):
    """
    用户登录
    :param username: 用户名
    :param password: 明文密码
    :return: string token
    """
    if not username:
        raise AppException('用户名不能为空')

    if not password:
        raise AppException('密码不能为空')

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
    :param username: 用户名
    :param password: 明文密码
    :param password_repeat: 重复密码
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


def permission(role=RoleEnum.ADMIN):
    """
    权限控制
    :param role:
    :return:
    """

    def outer_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if role is None:
                # 跳过权限校验
                pass
            else:
                current_user_id = g.user_id

                if not current_user_id:
                    raise AppException('用户未登录')

                user_row = UserModel.get_by_id(current_user_id)
                if not user_row:
                    raise AppException('用户不存在')

                if user_row.status != StatusEnum.Enabled:
                    raise AppException('用户已禁用')

                if not has_role_permission(current_role=user_row.role, need_permission=role):
                    raise AppException('暂无权限')

                # 当前用户数据全局可用
                g.current_user_row = user_row

            # execute
            ret = func(*args, **kwargs)

            return ret

        return wrapper

    return outer_wrapper


def has_role_permission(current_role, need_permission):
    """
    角色权限判断
    :param current_role:
    :param need_permission:
    :return:
    """
    if not need_permission:
        return True

    current_permission = []

    for item in ROLE_PERMISSION:
        if item['role'] == current_role:
            current_permission = item['permission']

    return need_permission in current_permission


@async_task_service.async_task_decorator("发送邮箱验证码")
def send_verify_code_async(email):
    send_verify_code(email)


def send_verify_code(email):
    if not validate_util.is_email(email):
        raise AppException('邮箱格式不正确')

    code = secret_util.get_random_password()

    cache_util.set_value(key=email, value=code, expire=5 * 60)

    notify_service.send_email_to_user(
        template='code-email.html',
        subject='验证码',
        data={'code': code},
        email_list=[email]
    )


def login_by_email(email, code):
    if not validate_util.is_email(email):
        raise AppException('邮箱格式不正确')

    if not code:
        raise AppException('验证码不能为空')

    cache_code = cache_util.get_value(email)

    if cache_code and code == cache_code:
        pass
    else:
        raise AppException('验证码不正确')

    user_row = UserModel.select().where(
        UserModel.username == email
    ).get_or_none()

    if not user_row:
        user_row = UserModel.create(
            username=email,
            password=''
        )

    return token_service.encode_token({
        'user_id': user_row.id
    })
