# -*- coding: utf-8 -*-
"""
@File    : test_demo.py
@Date    : 2022-11-05
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division


def test_index(client):
    response = client.get('/test')

    # fix:
    if hasattr(response, 'text'):
        text = response.text
    else:
        text = response.data.decode()

    assert 'hello' in text
