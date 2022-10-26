# -*- coding: utf-8 -*-

import os

# 项目的运行目录
RUNTIME_DIR = os.getcwd()

# 配置文件目录
CONFIG_DIR = os.path.dirname(__file__)

# 应用文件目录
APP_DIR = os.path.dirname(CONFIG_DIR)

# 项目根目录
ROOT_DIR = os.path.dirname(APP_DIR)

# 模板目录
TEMPLATE_DIR = os.path.join(APP_DIR, 'templates')

# 公开资源目录
PUBLIC_DIR = os.path.join(APP_DIR, 'public')

# 临时文件存放地
TEMP_DIR = os.path.join(RUNTIME_DIR, 'temp')
TEMP_DIR_BASE_URL = '/temp'

# 数据库文件存放
DATABASE_DIR = os.path.join(RUNTIME_DIR, 'database')

# sqlite 数据库
SQLITE_DATABASE_PATH = os.path.join(DATABASE_DIR, 'database.db')

# 日志文件夹
LOG_DIR = os.path.join(RUNTIME_DIR, 'logs')

# 创建文件夹
dir_list = [
    TEMP_DIR,
    DATABASE_DIR,
    LOG_DIR
]

for dirname in dir_list:
    if not os.path.exists(dirname):
        os.mkdir(dirname)

# 管理员账号，用户名
ADMIN_USERNAME = 'admin'

# header请求头中携带 token 参数名称
TOKEN_KEY = 'X-Token'
