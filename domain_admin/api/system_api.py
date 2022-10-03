# -*- coding: utf-8 -*-

from flask import request

from domain_admin.model.system_model import SystemModel
from domain_admin.service import scheduler_service
from domain_admin.utils import datetime_util


def update_system_config():
    """
    更新配置
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

    def hidden_value(item):
        if item.is_show_value == False:
            if item.value:
                item.value = '******'

        return item

    # lst = list(map(lambda x: hidden_value(x), lst))

    return {
        'list': lst,
        'total': len(lst)
    }
