# -*- coding: utf-8 -*-
"""
oidc_api.py
OpenID Connect API 端点
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from flask import redirect

from domain_admin.service import oidc_service
from domain_admin.utils.flask_ext.app_exception import AppException


def oidc_config():
    """
    获取 OIDC 配置信息
    返回给前端，用于判断是否显示 OIDC 登录按钮
    """
    return {
        'enabled': oidc_service.is_oidc_enabled()
    }


def oidc_login():
    """
    发起 OIDC 登录
    重定向到 OIDC 提供商的授权页面
    """
    # 检查 OIDC 是否启用
    if not oidc_service.is_oidc_enabled():
        raise AppException('OIDC 单点登录未启用')

    # 生成授权 URL 并重定向（authlib 自动处理 state）
    return oidc_service.get_authorization_url()


def oidc_callback():
    """
    OIDC 回调端点
    处理 OIDC 提供商的回调，完成登录
    """
    # 检查 OIDC 是否启用
    if not oidc_service.is_oidc_enabled():
        raise AppException('OIDC 单点登录未启用')

    # 处理回调，获取 token（authlib 自动处理授权码交换和 state 验证）
    jwt_token = oidc_service.handle_callback()

    # 调试时注意跳转的地址是否正确
    redirect_url = f"/?token={jwt_token}"
    return redirect(redirect_url)
