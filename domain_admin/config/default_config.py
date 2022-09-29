# -*- coding: utf-8 -*-

import os

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
