# -*- coding: utf-8 -*-
"""
@File    : conftest.py
@Date    : 2022-11-05
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import pytest
from flask.testing import FlaskClient

from domain_admin.main import app


@pytest.fixture()
def client():
    """
    FlaskClient
    :return:
    """
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        client = app.test_client()

        return client


@pytest.fixture()
def token(client):
    """
    str
    :param client:
    :return:
    """

    response = client.post('/api/login', json={
        'username': 'admin',
        'password': '123456'
    })

    return response.json['data']['token']
