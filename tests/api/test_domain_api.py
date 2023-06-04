# -*- coding: utf-8 -*-
"""
@File    : test_demo.py
@Date    : 2022-11-05
@Author  : Peng Shiyu
"""


def test_update_domain_cert_info_by_id(client, token):
    response = client.post(
        path='/api/updateDomainCertInfoById',
        json={
            'domain_id': 1
        },
        headers={'x-token': token}
    )

    print(response.json())
