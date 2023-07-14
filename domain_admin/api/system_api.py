# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
from flask import request

from domain_admin import version
from domain_admin.enums.config_key_enum import ConfigKeyEnum
from domain_admin.model.system_model import SystemModel
from domain_admin.service import scheduler_service
from domain_admin.utils import datetime_util


def update_system_config():
    """
    更新单个配置
    :return:
    """
    allow_keys = [
        ConfigKeyEnum.MAIL_HOST,
        ConfigKeyEnum.MAIL_PORT,
        ConfigKeyEnum.MAIL_ALIAS,
        ConfigKeyEnum.MAIL_USERNAME,
        ConfigKeyEnum.MAIL_PASSWORD,
    ]

    for key in allow_keys:
        value = request.json[key]

        SystemModel.update(
            {
                'value': value,
                'update_time': datetime_util.get_datetime()
            }
        ).where(
            SystemModel.key == key
        ).execute()


def get_all_system_config():
    """
    获取所有配置项
    :return:
    """
    lst = SystemModel.select().where(
        SystemModel.key.in_([
            ConfigKeyEnum.MAIL_HOST,
            ConfigKeyEnum.MAIL_PORT,
            ConfigKeyEnum.MAIL_ALIAS,
            ConfigKeyEnum.MAIL_USERNAME,
            ConfigKeyEnum.MAIL_PASSWORD,
        ])
    )

    return {item.key: item.value for item in lst}


def get_system_env_config():
    """
    获取配置项
    :return:
    """
    lst = SystemModel.select().where(
        SystemModel.key.in_([
            ConfigKeyEnum.PROMETHEUS_KEY
        ])
    )

    return {item.key: item.value for item in lst}


def get_cron_config():
    """
    获取配置项
    :return:
    """
    lst = SystemModel.select().where(
        SystemModel.key.in_([
            ConfigKeyEnum.SCHEDULER_CRON
        ])
    )

    return {item.key: item.value for item in lst}


def update_cron_config():
    """
    更新cron配置
    :return:
    """
    scheduler_cron = request.json['scheduler_cron']

    SystemModel.update(
        {
            'value': scheduler_cron,
            'update_time': datetime_util.get_datetime()
        }
    ).where(
        SystemModel.key == ConfigKeyEnum.SCHEDULER_CRON
    ).execute()

    # 更新定时
    scheduler_service.update_job(scheduler_cron)


def get_system_version():
    """
    获取当前应用版本号
    :return:
    """
    return {
        'version': version.VERSION
    }
