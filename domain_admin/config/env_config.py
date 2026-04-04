# -*- coding: utf-8 -*-
"""
@File    : env_config.py
@Date    : 2023-06-13
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from environs import Env
from .default_config import *

env = Env()

# read .env file, if it exists
env.read_env()

# database
DB_CONNECT_URL = env.str("DB_CONNECT_URL", DEFAULT_DB_CONNECT_URL)

# 初始化 管理员账号，用户名
ADMIN_USERNAME = env.str("ADMIN_USERNAME", DEFAULT_ADMIN_USERNAME)
ADMIN_PASSWORD = env.str("ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD)

# prometheus key
PROMETHEUS_KEY = env.str("PROMETHEUS_KEY", DEFAULT_PROMETHEUS_KEY)

# secret_key
SECRET_KEY = env.str("SECRET_KEY", DEFAULT_SECRET_KEY)

# token_expire_days
TOKEN_EXPIRE_DAYS = env.int("TOKEN_EXPIRE_DAYS", DEFAULT_TOKEN_EXPIRE_DAYS)

# APP_MODE : production, development
APP_MODE = env.str("APP_MODE", 'production')

# ALLOW_COMMANDS
ALLOW_COMMANDS = [cmd.strip() for cmd in env.str("ALLOW_COMMANDS", '').split(';') if cmd.strip()]

# ENABLED_REGISTER
ENABLED_REGISTER = env.bool("ENABLED_REGISTER", False)

# OIDC 单点登录配置
OIDC_ENABLED = env.bool("OIDC_ENABLED", OIDC_ENABLED)
OIDC_CLIENT_ID = env.str("OIDC_CLIENT_ID", "")
OIDC_CLIENT_SECRET = env.str("OIDC_CLIENT_SECRET", "")
OIDC_ISSUER_URL = env.str("OIDC_ISSUER_URL", "")
OIDC_SCOPES = env.str("OIDC_SCOPES", "openid profile email")

# OIDC 自动创建用户的默认配置
OIDC_AUTO_CREATE_USER_ROLE = env.int("OIDC_AUTO_CREATE_USER_ROLE", 1)  # 1=USER, 10=ADMIN
OIDC_AUTO_CREATE_USER_STATUS = env.bool("OIDC_AUTO_CREATE_USER_STATUS", False)
