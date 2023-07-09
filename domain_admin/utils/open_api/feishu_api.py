# -*- coding: utf-8 -*-
"""
@File    : feishu_api.py
@Date    : 2023-06-22

飞书开放API接口
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import requests


def get_access_token(app_id, app_secret):
    """
    自建应用获取 tenant_access_token
    https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant_access_token_internal

    :param app_id: 应用唯一标识
    :param app_secret: 应用秘钥
    :return:
    {
        "code": 0,
        "msg": "success",
        "tenant_access_token": "t-caecc734c2e3328a62489fe0648c4b98779515d3",
        "expire": 7140
    }
    """
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'

    params = {
        'app_id': app_id,
        'app_secret': app_secret
    }

    res = requests.post(url, params=params)

    return res.json()


def send_message(access_token, body, params):
    """
    发送消息
    https://open.feishu.cn/document/server-docs/im-v1/message/create

    :param access_token:
    :param body: 消息体
    :param params: 查询参数 {"receive_id_type":"open_id"}
    :return:
    """

    url = 'https://open.feishu.cn/open-apis/im/v1/messages'

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    res = requests.post(url, params=params, headers=headers, json=body)
    return res.json()
