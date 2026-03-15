# -*- coding: utf-8 -*-
"""
oidc_service.py
OpenID Connect 单点登录服务
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from authlib.integrations.flask_client import OAuth
from flask import url_for

from domain_admin.log import logger
from domain_admin.model.user_model import UserModel
from domain_admin.service import token_service
from domain_admin.utils.flask_ext.app_exception import AppException

# OAuth 实例
oauth = OAuth()


def init_oidc(app):
    """
    初始化 OIDC OAuth 客户端
    :param app: Flask 应用实例
    """
    try:
        if not is_oidc_enabled():
            logger.info("OIDC 单点登录未启用，跳过初始化")
            return

        # 初始化 OAuth
        oauth.init_app(app)

        # 获取配置
        config = get_oidc_config()
        client_id = config.get('client_id')
        client_secret = config.get('client_secret')
        issuer_url = config.get('issuer_url')
        scopes = config.get('scopes', 'openid profile email')

        if not all([client_id, client_secret, issuer_url]):
            logger.warning("OIDC 配置不完整，跳过初始化")
            return

        # 注册 OIDC 客户端（authlib 会自动存储，可通过 oauth.oidc 访问）
        oauth.register(
            name='oidc',
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=f"{issuer_url}/.well-known/openid-configuration",
            client_kwargs={
                'scope': scopes
            }
        )

        logger.info("OIDC OAuth 客户端初始化成功")

    except Exception as e:
        logger.error(f"OIDC 初始化失败: {str(e)}")
        # 优雅降级 - 不让应用崩溃


def is_oidc_enabled():
    """
    检查 OIDC 是否启用
    :return: bool
    """
    from domain_admin.config import OIDC_ENABLED
    return OIDC_ENABLED


def get_oidc_config():
    """
    Get OIDC configuration from environment variables
    :return: dict with keys: issuer_url, client_id, client_secret, scopes
    """
    from domain_admin.config import (
        OIDC_ISSUER_URL, OIDC_CLIENT_ID, OIDC_CLIENT_SECRET, OIDC_SCOPES,
        OIDC_AUTO_CREATE_USER_ROLE, OIDC_AUTO_CREATE_USER_STATUS
    )

    return {
        'issuer_url': OIDC_ISSUER_URL,
        'client_id': OIDC_CLIENT_ID,
        'client_secret': OIDC_CLIENT_SECRET,
        'scopes': OIDC_SCOPES,
        'auto_create_user_role': OIDC_AUTO_CREATE_USER_ROLE,
        'auto_create_user_status': OIDC_AUTO_CREATE_USER_STATUS
    }


def get_authorization_url():
    """
    生成授权 URL 并重定向
    :return: Flask redirect response
    """
    if not hasattr(oauth, 'oidc'):
        raise AppException("OIDC 客户端未初始化")

    # 动态构建完整的 redirect_uri
    # 使用 url_for 生成回调地址，_external=True 生成完整 URL
    redirect_uri = url_for('oidc_callback', _external=True)
    return oauth.oidc.authorize_redirect(redirect_uri)


def handle_callback():
    """
    处理 OIDC 回调
    :return: JWT token
    """
    if not hasattr(oauth, 'oidc'):
        raise AppException("OIDC 客户端未初始化")

    try:
        logger.info("开始处理 OIDC 回调")

        # 交换授权码获取 token
        token = oauth.oidc.authorize_access_token()
        logger.info(f"Token 交换成功，token keys: {token.keys() if token else 'None'}")

        # 获取用户信息
        userinfo = token.get('userinfo')
        if not userinfo:
            # 如果 token 中没有 userinfo，从 userinfo 端点获取
            logger.info("从 userinfo 端点获取用户信息")
            userinfo = oauth.oidc.userinfo(token=token)

        logger.info(f"用户信息获取成功: {userinfo.keys() if userinfo else 'None'}")

        # 处理用户登录或注册
        return process_oidc_user(userinfo)

    except AppException:
        raise
    except Exception as e:
        logger.error(f"OIDC 回调处理失败: {str(e)}")
        raise AppException(f"OIDC 认证失败: {str(e)}")


def process_oidc_user(userinfo):
    """
    处理 OIDC 用户信息，创建或更新用户
    :param userinfo: OIDC 用户信息
    :return: JWT token
    """
    # 从 userinfo 中提取用户标识
    # 优先使用 preferred_username，其次使用 email，最后使用 sub
    username = userinfo.get('preferred_username') or userinfo.get('email') or userinfo.get('sub')

    if not username:
        raise AppException('无法从 OIDC 提供商获取用户标识')

    logger.info(f"处理 OIDC 用户: {username}")

    # 查找或创建用户
    user_row = UserModel.select().where(
        UserModel.username == username
    ).get_or_none()

    if not user_row:
        # 自动创建用户
        oidc_config = get_oidc_config()
        user_row = UserModel.create(
            username=username,
            password='',  # OIDC 用户不需要密码
            role=oidc_config['auto_create_user_role'],
            status=oidc_config['auto_create_user_status'],
            avatar_url=userinfo.get('picture', '')
        )
        logger.info(f"创建新用户: {username}")
    else:
        logger.info(f"用户已存在: {username}")

    # 生成 JWT token
    return token_service.encode_token({
        'user_id': user_row.id
    })
