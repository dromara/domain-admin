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
from domain_admin.migrate import migrate_110_to_1212
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

        # 2023-04-22
        if local_version in [
            VersionEnum.Version_110,
            VersionEnum.Version_111,
            VersionEnum.Version_112,
            VersionEnum.Version_113,
            VersionEnum.Version_114,
            VersionEnum.Version_115,
            VersionEnum.Version_116,
            VersionEnum.Version_117,
            VersionEnum.Version_118,
            VersionEnum.Version_119,
            VersionEnum.Version_1110,
            VersionEnum.Version_120,
            VersionEnum.Version_121,
            VersionEnum.Version_122,
            VersionEnum.Version_123,
            VersionEnum.Version_124,
            VersionEnum.Version_128,
            VersionEnum.Version_129,
            VersionEnum.Version_1210,
            VersionEnum.Version_1211,
        ]:
            # some => 1.2.12
            logger.info('update version: %s => %s', local_version, VersionEnum.Version_1212)
            migrate_110_to_1212.execute_migrate()
            local_version = VersionEnum.Version_1212

    # 更新版本号
    VersionModel.create(
        version=current_version
    )
