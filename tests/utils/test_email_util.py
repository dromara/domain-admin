# -*- coding: utf-8 -*-
"""
@File    : test_email_util.py
@Date    : 2023-07-01
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from domain_admin.utils import email_util


def test_send_email():
    email_util.send_email(
        mail_host='localhost',
        mail_port=8081,
        subject='测试',
        content='内容',
        to_addresses=['user@example.com'],
    )
