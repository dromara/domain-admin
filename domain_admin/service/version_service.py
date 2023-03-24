# -*- coding: utf-8 -*-
"""
@File    : version_service.py
@Date    : 2022-11-02
@Author  : Peng Shiyu
"""
from domain_admin.enums.version_enum import VersionEnum
from domain_admin.log import logger
from domain_admin.migrate import migrate_102_to_103
from domain_admin.migrate import migrate_106_to_110
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

    # 版本号校验
    if local_version == current_version:
        return

    # 版本不一致才需要升级
    if local_version is not None:
        if local_version in [
            VersionEnum.Version_100,
            VersionEnum.Version_101,
            VersionEnum.Version_102,
        ]:
            # 1.0.0 1.0.1 1.0.2 => 1.0.3
            logger.info('update version: %s => %s', local_version, VersionEnum.Version_103)
            migrate_102_to_103.execute_migrate()
            local_version = VersionEnum.Version_103

        # 2023-03-24
        if local_version in [
            VersionEnum.Version_103,
            VersionEnum.Version_104,
            VersionEnum.Version_105,
            VersionEnum.Version_106,
        ]:
            # 1.0.3 1.0.4 1.0.5 1.0.6 => 1.1.0
            logger.info('update version: %s => %s', local_version, VersionEnum.Version_110)
            migrate_106_to_110.execute_migrate()
            local_version = VersionEnum.Version_110

        # else:
            # raise Exception('version update not support: {} => {}'.format(local_version, current_version))


    # 更新版本号
    VersionModel.create(
        version=current_version
    )
