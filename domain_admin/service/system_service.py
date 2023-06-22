# -*- coding: utf-8 -*-
"""
system_service.py
"""
from domain_admin.enums.config_key_enum import ConfigKeyEnum
from domain_admin.model.system_model import SystemModel
from domain_admin.utils.flask_ext.app_exception import AppException


def get_system_config():
    """
    获取系统配置
    :return:
    """
    rows = SystemModel.select(
        SystemModel.key,
        SystemModel.value,
    )

    config = {}
    for row in rows:
        config[row.key] = row.value

    return config


def get_config(key):
    return get_system_config().get(key)


def check_email_config(config):
    if not config['mail_host']:
        raise AppException('未设置发件邮箱服务器地址')

    if not config['mail_port']:
        raise AppException('未设置发件邮箱服务器端口')

    if not config['mail_username']:
        raise AppException('未设置发件人邮箱账号')

    if not config['mail_password']:
        raise AppException('未设置发件人邮箱密码')


def get_email_config():
    config = get_system_config()

    check_email_config(config)

    return config


def init_system_config(app):
    """
    初始化全局常量配置
    :param app:
    :return:
    """
    config = get_system_config()

    app.config[ConfigKeyEnum.SECRET_KEY] = config[ConfigKeyEnum.SECRET_KEY]
    app.config[ConfigKeyEnum.TOKEN_EXPIRE_DAYS] = config[ConfigKeyEnum.TOKEN_EXPIRE_DAYS]
