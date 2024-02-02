# -*- coding: utf-8 -*-
"""
@File    : domain_info_model_test.py
@Date    : 2024-01-30
@Author  : Peng Shiyu
"""
import unittest

from peewee import SQL

from domain_admin.model.domain_info_model import DomainInfoModel


class MonitorServiceTest(unittest.TestCase):
    def test_add(self):
        DomainInfoModel.update(
            version=DomainInfoModel.version + 1
        ).where(
            DomainInfoModel.id == 1
        ).execute()

    # ('UPDATE `tb_domain_info` SET `version` = (`tb_domain_info`.`version` + %s) WHERE (`tb_domain_info`.`id` = %s)', [1, 1])

    def test_order(self):
        rows = list(DomainInfoModel.select(
            DomainInfoModel.id, DomainInfoModel.create_time
        ).order_by(SQL("`create_time` desc")))

        # ('SELECT `t1`.`id`, `t1`.`create_time` FROM `tb_domain_info` AS `t1` ORDER BY `create_time` desc', [])

    def test_in(self):
        rows = list(DomainInfoModel.select(
            DomainInfoModel.id, DomainInfoModel.create_time
        ).where(
            DomainInfoModel.id.in_([1, 2, 3])
        ))

        # ('SELECT `t1`.`id`, `t1`.`create_time` FROM `tb_domain_info` AS `t1` WHERE (`t1`.`id` IN (%s, %s, %s))', [1, 2, 3])
