# -*- coding: utf-8 -*-

from flask import request

from domain_admin.service import auth_service


def login():
    """
    用户登录
    :return:
    """
    username = request.json['username']
    password = request.json['password']

    token = auth_service.login(username, password)

    return {'token': token}


def register():
    """
    用户注册
    :return:
    """
    username = request.json['username']
    password = request.json['password']
    password_repeat = request.json['password_repeat']

    auth_service.register(username, password, password_repeat)
