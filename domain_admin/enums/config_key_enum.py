# -*- coding: utf-8 -*-
"""
@File    : config_key_enum.py
@Date    : 2023-06-16
"""
from __future__ import print_function, unicode_literals, absolute_import, division

class ConfigKeyEnum(object):
    """
    系统配置key键名常量
    """
    # 发件邮箱服务器地址
    MAIL_HOST = 'mail_host'

    # 发件邮箱服务器端口
    MAIL_PORT = 'mail_port'

    # 发件人邮箱名称
    MAIL_ALIAS = 'mail_alias'

    # 发件人邮箱密码
    MAIL_USERNAME = 'mail_username'

    # 发件人邮箱密码
    MAIL_PASSWORD = 'mail_password'

    # 邮件标题
    # @Deprecated @since 1.4.4
    MAIL_SUBJECT = 'mail_subject'

    # 定时检测时间（crontab 表达式）
    SCHEDULER_CRON = 'scheduler_cron'

    # Token秘钥
    SECRET_KEY = 'secret_key'

    # Token有效期（天）
    TOKEN_EXPIRE_DAYS = 'token_expire_days'

    # prometheus_key
    PROMETHEUS_KEY = 'prometheus_key'
