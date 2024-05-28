# -*- coding: utf-8 -*-
"""
@File    : telegram_api.py
@Date    : 2024-05-28
"""
import requests


def send_message(bot, token, chat_id, text):
    """
    发送应用消息
    :return:
    """
    url = 'https://api.telegram.org/{bot}:{token}/sendMessage'.format(
        bot=bot,
        token=token
    )

    params = {
        'chat_id': chat_id,
        'text': text,
    }

    res = requests.post(url, data=params)
    return res.json()
