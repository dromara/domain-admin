# -*- coding: utf-8 -*-
"""
@File    : version_service.py
@Date    : 2022-11-02
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from peewee import IntegrityError

from domain_admin.enums.version_enum import VersionEnum
from domain_admin.log import logger
from domain_admin.migrate import migrate

from domain_admin.model.version_model import VersionModel
from domain_admin.version import VERSION


def get_local_version():
    """
    获取本地最新版本号
    :return:
    """
    row = VersionModel.select().order_by(
        VersionModel.create_time.desc()
    ).get_or_none()

    if row:
        return row.version


def get_current_version():
    """
    获取当前版本号
    :return:
    """
    return VERSION


def update_version():
    """
    版本升级
    :return:
    """
    local_version = get_local_version()
    current_version = get_current_version()
    logger.info("local_version: %s => current_version: %s", local_version, current_version)

    # 版本号校验
    if local_version == current_version:
        return

    # 版本不一致才需要升级
    if local_version is not None:
        migrate.execute_migrate(local_version)

    # 更新版本号
    # fix: 多实例同时启动版本号写入失败问题
    try:
        VersionModel.create(
            version=current_version
        )
    except IntegrityError:
        pass
