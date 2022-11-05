# -*- coding: utf-8 -*-
"""
@File    : test_demo.py
@Date    : 2022-11-05
@Author  : Peng Shiyu
"""


def test_index(client):
    response = client.get('/')
    assert 'id="app"' in response.text
