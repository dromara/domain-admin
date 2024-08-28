# -*- coding: utf-8 -*-
"""
@File    : migrate_1647_to_1648.py
@Date    : 2024-08-28

cmd:
$ python domain_admin/migrate/migrate_1647_to_1648.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.config import ADMIN_USERNAME
from domain_admin.enums.role_enum import RoleEnum
from domain_admin.migrate import migrate_common
from domain_admin.model.base_model import db
from domain_admin.model.issue_certificate_model import IssueCertificateModel, DeployStatusEnum
from domain_admin.model.tag_model import TagModel
from domain_admin.model.user_model import UserModel


def execute_migrate():
    """
    版本升级 1.6.47 => 1.6.48
    :return:
    """
    UserModel.update(
        role=RoleEnum.ADMIN
    ).where(
        UserModel.username == ADMIN_USERNAME
    ).execute()
