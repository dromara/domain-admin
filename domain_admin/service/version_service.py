# -*- coding: utf-8 -*-
"""
@File    : version_service.py
@Date    : 2022-11-02
@Author  : Peng Shiyu
"""
from domain_admin.enums.version_enum import VersionEnum
from domain_admin.migrate import migrate_102_to_103
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

    if local_version is None:
        pass
    elif local_version == VersionEnum.Version_102:
        # 1.0.2 => 1.0.3
        migrate_102_to_103.execute_migrate()
    else:
        raise Exception('version update not support: {} => {}'.format(local_version, current_version))

    # 更新版本号
    VersionModel.create(
        version=current_version
    )
