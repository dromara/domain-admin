# -*- coding: utf-8 -*-
"""
@File    : monitor_service_test.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""
import json
import unittest

from domain_admin.enums.monitor_type_enum import MonitorTypeEnum
from domain_admin.enums.role_enum import RoleEnum
from domain_admin.model.monitor_model import MonitorModel
from domain_admin.service import monitor_service, auth_service


class AuthServiceTest(unittest.TestCase):
    def test_has_role_permission(self):
        assert auth_service.has_role_permission(current_role=None, need_permission=RoleEnum.USER) is False
        assert auth_service.has_role_permission(current_role=RoleEnum.USER, need_permission=RoleEnum.ADMIN) is False
        assert auth_service.has_role_permission(current_role=RoleEnum.ADMIN, need_permission=RoleEnum.USER) is True
        assert auth_service.has_role_permission(current_role=RoleEnum.ADMIN, need_permission=RoleEnum.ADMIN) is True
        assert auth_service.has_role_permission(current_role=RoleEnum.USER, need_permission=RoleEnum.USER) is True
        assert auth_service.has_role_permission(current_role=RoleEnum.USER, need_permission=None) is True

    def test_send_verify_code(self):
        auth_service.send_verify_code('xxx@qq.com')
