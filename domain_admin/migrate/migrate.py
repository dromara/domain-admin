# -*- coding: utf-8 -*-
"""
@File    : migrate.py
@Date    : 2023-09-24
"""
from domain_admin.log import logger
from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.migrate.migrate_config import MIGRATE_CONFIG


def execute_migrate(local_version):
    """
    数据库升级
    :param local_version: 本地最新版本
    :return:
    """

    for config in MIGRATE_CONFIG:
        local_versions = config['local_versions']
        update_version = config['update_version']
        migrate_func = config['migrate_func']

        if local_version in local_versions:
            logger.info('update version: %s => %s', local_version, update_version)
            migrate_func()
            local_version = update_version
