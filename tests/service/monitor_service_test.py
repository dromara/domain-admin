# -*- coding: utf-8 -*-
"""
@File    : monitor_service_test.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""
import json
import unittest

from domain_admin.enums.monitor_type_enum import MonitorTypeEnum
from domain_admin.model.monitor_model import MonitorModel
from domain_admin.service import monitor_service


class MonitorServiceTest(unittest.TestCase):
    def test_add_monitor(self):
        MonitorModel.create(
            title='测试',
            monitor_type=MonitorTypeEnum.HTTP,
            content=json.dumps({
                'url': 'http://www.baidu.com', 'method': 'GET', 'timeout': 10
            }),
            interval=10,
        )

    def test_run_monitor_task(self):
        monitor_service.run_monitor_task()

    def test_run_http_monitor(self):
        url = 'https://www.qq.com/'
        url = 'https://www.163.com/'
        url = 'https://httpbin.org/get'
        url = 'https://www.csdn.net/'
        ret = monitor_service.run_http_monitor(url, method='GET', timeout=3)
        print(ret)
