# -*- coding: utf-8 -*-
"""
@File    : ding_talk_api.py
@Date    : 2023-06-22

钉钉开放API接口
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import requests


def get_access_token(appkey, appsecret):
    """
    获取access_token
    https://open.dingtalk.com/document/orgapp/obtain-orgapp-token

    :param appkey: 应用的唯一标识key
    :param appsecret: 应用的密钥
    :return:
    {
        "errcode": 0,
        "access_token": "96fc7a7axxx",
        "errmsg": "ok",
        "expires_in": 7200
    }
    """
    url = 'https://oapi.dingtalk.com/gettoken'
    params = {
        'appkey': appkey,
        'appsecret': appsecret
    }

    res = requests.get(url, params=params)
    return res.json()


def send_message(access_token, body):
    """
    发送应用消息
    https://open.dingtalk.com/document/orgapp/asynchronous-sending-of-enterprise-session-messages

    :param access_token:
    :param body: 消息体
    :return:

    {
        "errcode":0,
        "task_id":256271667526,
        "request_id":"4jzllmte0wau"
    }
    """
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2'

    params = {
        'access_token': access_token,
    }

    res = requests.post(url, params=params, json=body)
    return res.json()
