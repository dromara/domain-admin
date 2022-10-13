# -*- coding: utf-8 -*-

from flask import request

from domain_admin import version
from domain_admin.model.system_model import SystemModel
from domain_admin.service import scheduler_service
from domain_admin.utils import datetime_util


def update_system_config():
    """
    更新单个配置
    :return:
    """
    key = request.json['key']
    value = request.json['value']

    SystemModel.update(
        {
            'value': value,
            'update_time': datetime_util.get_datetime()
        }
    ).where(
        SystemModel.key == key
    ).execute()

    # 更新定时
    if key == 'scheduler_cron':
        scheduler_service.update_job(value)


def get_all_system_config():
    """
    获取所有配置项
    :return:
    """
    lst = SystemModel.select()

    return {
        'list': lst,
        'total': len(lst)
    }


def get_system_version():
    """
    获取当前应用版本号
    :return:
    """
    return {
        'version': version.VERSION
    }
