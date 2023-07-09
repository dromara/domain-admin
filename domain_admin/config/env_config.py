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
