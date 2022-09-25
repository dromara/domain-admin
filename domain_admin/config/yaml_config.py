# -*- coding: utf-8 -*-

#################################
# 读取用户自定义变量
#################################

import os

import yaml

config_file = os.path.join(os.getcwd(), 'config.yml')

# logger.info('config_file: %s', config_file)

if os.path.exists(config_file):
    f = open(config_file, "rb")
    config = yaml.safe_load(f)
    f.close()
else:
    config = {}

##############################
#            邮箱配置
##############################
# 服务器地址
MAIL_HOST = config.get('MAIL_HOST')
# 服务器端口 25 或者 465(ssl)
MAIL_PORT = config.get('MAIL_PORT')

# 发件人邮箱账号
MAIL_USERNAME = config.get('MAIL_USERNAME')
# 发件人邮箱密码
MAIL_PASSWORD = config.get('MAIL_PASSWORD')

# 到期前几天邮件提醒
BEFORE_EXPIRE_DAYS = config.get('BEFORE_EXPIRE_DAYS')

# 提醒邮箱
MAIL_TO_ADDRESSES = config.get('MAIL_TO_ADDRESSES')