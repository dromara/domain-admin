# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
from flask import request

from domain_admin.service import auth_service
from domain_admin.utils.flask_ext.app_exception import AppException


def login():
    """
    用户登录
    :return:
    """
    username = request.json['username']
    password = request.json['password']

    token = auth_service.login(username, password)

    return {'token': token}


def login_by_email():
    """
    邮箱登录
    :return:
    """

    email = request.json['email']
    code = request.json['code']

    token = auth_service.login_by_email(email, code)

    return {'token': token}


def send_code():
    """
    发送验证码
    :return:
    """
    email = request.json['email']

    auth_service.send_verify_code_async(email)
