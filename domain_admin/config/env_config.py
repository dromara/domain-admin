# -*- coding: utf-8 -*-
"""
@File    : env_config.py
@Date    : 2023-06-13
"""
from environs import Env
from .default_config import *

env = Env()

# read .env file, if it exists
env.read_env()

# database
DB_CONNECT_URL = env.str("DB_CONNECT_URL", "sqlite:///database/database.db")

# 管理员账号，用户名
ADMIN_USERNAME = env.str("ADMIN_USERNAME", ADMIN_USERNAME)
ADMIN_PASSWORD = env.str("ADMIN_PASSWORD", ADMIN_PASSWORD)
