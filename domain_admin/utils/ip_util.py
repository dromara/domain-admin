# -*- coding: utf-8 -*-
"""
@File    : ip_util.py
@Date    : 2022-10-13
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import requests


def get_ip_info(ip):
    """
    获取ip地址的信息
    :param ip: str
    :return:
    """

    url = 'http://ip.taobao.com/outGetIpInfo'

    params = {
        'ip': ip,
        'accessKey': 'alibaba-inc'
    }
    res = requests.get(url, params)

    if not res.ok:
        res.raise_for_status()

    return res.json().get('data')


if __name__ == '__main__':
    print(get_ip_info('221.218.209.125'))

