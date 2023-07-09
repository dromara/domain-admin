# -*- coding: utf-8 -*-
"""
@File    : test_text_util.py
@Date    : 2023-05-30
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from domain_admin.utils import text_util


def test_has_chinese():
    assert text_util.has_chinese("I love you") is False
    assert text_util.has_chinese("我喜欢你") is True
    assert text_util.has_chinese("我 love 你") is True
