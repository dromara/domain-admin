# -*- coding: utf-8 -*-
"""
@File    : telegram_api.py
@Date    : 2024-05-28
"""
import requests


def send_message(token, chat_id, text, proxies):
    """
    发送应用消息
    ref https://mp.weixin.qq.com/s/dvQiP87LQYP7ssx4zELb1w
    :return:
    """
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(
        token=token
    )

    data = {
        'chat_id': chat_id,
        'text': text,
    }

    res = requests.post(url=url, data=data, proxies=proxies)
    return res.json()
