# -*- coding: utf-8 -*-

from flask import request

from domain_admin.service import auth_service


def add_user():
    """
    添加用户
    :return:
    """
    username = request.json['username']
    password = request.json['password']
    password_repeat = request.json['password_repeat']

    auth_service.register(username, password, password_repeat)
