# -*- coding: utf-8 -*-
"""
@File    : api.py
@Date    : 2023-03-08

企业微信开放API接口
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import requests


def get_access_token(corpid, corpsecret):
    """
    获取access_token
    https://developer.work.weixin.qq.com/document/path/91039

    :param corpid: 企业ID
    :param corpsecret: 应用的凭证密钥
    :return:
    {
       "errcode": 0,
       "errmsg": "ok",
       "access_token": "accesstoken000001",
       "expires_in": 7200
    }
    """
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    params = {
        'corpid': corpid,
        'corpsecret': corpsecret
    }

    res = requests.get(url, params=params)
    return res.json()


def send_message(access_token, body):
    """
    发送应用消息
    https://developer.work.weixin.qq.com/document/path/90236

    :param access_token:
    :param body: 消息体
    :return:

    {
      "errcode" : 0,
      "errmsg" : "ok",
      "invaliduser" : "userid1|userid2",
      "invalidparty" : "partyid1|partyid2",
      "invalidtag": "tagid1|tagid2",
      "unlicenseduser" : "userid3|userid4",
      "msgid": "xxxx",
      "response_code": "xyzxyz"
    }
    """
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send'

    params = {
        'access_token': access_token,
    }

    res = requests.post(url, params=params, json=body)
    return res.json()
