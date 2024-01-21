# -*- coding: utf-8 -*-
"""
@File    : test_text_util.py
@Date    : 2023-05-30
"""
from __future__ import print_function, unicode_literals, absolute_import, division
from domain_admin.utils import text_util
import unittest


class TextUtilTest(unittest.TestCase):
    def test_has_chinese(self):
        assert text_util.has_chinese("I love you") is False
        assert text_util.has_chinese("我喜欢你") is True
        assert text_util.has_chinese("我 love 你") is True

    def test_split_string(self):
        print(text_util.split_string('小明、小花、小红'))
        print(text_util.split_string('-、小明、小花、小红、-'))
        print(text_util.split_string(' 小明、 小花、 小红、-  、 、'))
