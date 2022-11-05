# -*- coding: utf-8 -*-
"""
@File    : auth_api.py
@Date    : 2022-11-05
@Author  : Peng Shiyu
"""


def test_login(client):
    response = client.post('/api/login', json={
        'username': 'admin',
        'password': '123456'
    })

    assert response.json['code'] == 0
