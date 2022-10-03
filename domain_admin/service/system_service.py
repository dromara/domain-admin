# -*- coding: utf-8 -*-
from domain_admin.model.system_model import SystemModel


def get_system_config():
    """
    获取系统配置
    :return:
    """
    rows = SystemModel.select()

    config = {}
    for row in rows:
        config[row.key] = row.value

    return config
