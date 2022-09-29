# -*- coding: utf-8 -*-
"""
user_service.py
"""
from domain_admin.config import ROOT_USERNAME, ROOT_PASSWORD
from domain_admin.service import auth_service


def init_root_user():
    """
    初始化root 管理员 账号
    :return:
    """
    try:
        auth_service.register(
            username=ROOT_USERNAME,
            password=ROOT_PASSWORD,
            password_repeat=ROOT_PASSWORD
        )
    except Exception:
        pass
