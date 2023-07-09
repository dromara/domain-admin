# -*- coding: utf-8 -*-
"""
@File    : test_cert.py
@Date    : 2022-11-05
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division


def test_get_cert_information_not_login(client):
    response = client.post('/api/getCertInformation')
    assert response.json['code'] == 401


def test_get_cert_information_not_params(client, token):
    response = client.post(
        path='/api/getCertInformation',
        headers={'x-token': token}
    )

    assert response.json['code'] == -1


def test_get_cert_information(client, token):
    response = client.post('/api/getCertInformation', json={
        'domain': 'www.baidu.com'
    }, headers={'x-token': token})

    assert response.json['code'] == 0
