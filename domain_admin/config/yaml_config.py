# -*- coding: utf-8 -*-

#################################
# 读取用户自定义变量
#################################

import os

from domain_admin.utils.yaml_util import read_yaml_file

CONFIG_FILE_NAME = 'config.yml'

config_file = os.path.join(os.getcwd(), CONFIG_FILE_NAME)

if os.path.exists(config_file):
    config = read_yaml_file(config_file)
else:
    config = {}

# ###### 邮箱配置 #######

# 服务器地址
MAIL_HOST = config.get('MAIL_HOST')
# 服务器端口 25 或者 465(ssl)
MAIL_PORT = config.get('MAIL_PORT')

# 发件人邮箱账号
MAIL_USERNAME = config.get('MAIL_USERNAME')
# 发件人邮箱密码
MAIL_PASSWORD = config.get('MAIL_PASSWORD')

# ###### 服务器配置 #######

# 服务器地址
FLASK_HOST = config.get('FLASK_HOST', '127.0.0.1')

# 服务器端口
FLASK_PORT = config.get('FLASK_PORT', 5000)

# 定时检测时间 分 时 日 月 周，默认每天上午 10: 30 检测
SCHEDULER_CRON = config.get('SCHEDULER_CRON', "30 10 * * *")

# ###### 账号权限配置 #######

# token key
SECRET_KEY = config.get('SECRET_KEY', "qzmPs4lP3t1GuM2tj38/7Qg5fqFsHPKBFz3KvZdy+GQ=")

# token 有效期 7 天
TOKEN_EXPIRE_DAYS = config.get('TOKEN_EXPIRE_DAYS', 7)

# 管理员账号
ROOT_USERNAME = config.get('ROOT_USERNAME', 'root')

# 管理员密码
ROOT_PASSWORD = config.get('ROOT_PASSWORD', '123456')
