# -*- coding: utf-8 -*-
"""
@File    : crtsh_api.py
@Date    : 2023-07-10

参考:
https://crt.sh/
https://github.com/PaulSec/crt.sh

需求：https://github.com/mouday/domain-admin/issues/41
"""

from __future__ import print_function, unicode_literals, absolute_import, division
import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'


def search(domain):
    """
    搜索子域证书列表
    :param domain: str 顶级域名
    :return:
    """
    url = "https://crt.sh/"

    params = {
        'q': domain,
        'output': 'json'
    }

    headers = {
        'User-Agent': USER_AGENT
    }

    req = requests.get(url=url, params=params, headers=headers)

    return req.json()


if __name__ == '__main__':
    lst = search('bilibili.com')
    print([row['common_name'] for row in lst])
