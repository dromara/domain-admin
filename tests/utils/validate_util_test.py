# -*- coding: utf-8 -*-
"""
@File    : validate_util_test.py
@Date    : 2024-01-31
@Author  : Peng Shiyu
"""
import unittest

from domain_admin.utils import validate_util


class ValidateUtilTest(unittest.TestCase):
    def test_has_chinese(self):
        assert validate_util.is_domain('13760613402@163.com') == False
        assert validate_util.is_domain('alleyliang@163.com') == False
        assert validate_util.is_domain('*.dai.163.com') == False
