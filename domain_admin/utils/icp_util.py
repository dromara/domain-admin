# -*- coding: utf-8 -*-
"""
@File    : icp_util.py
@Date    : 2023-06-30
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import requests

from domain_admin.utils import json_util


def get_icp(domain):
    """
    查询域名备案信息
    doc: https://api.vvhan.com/beian.html

    其他方式：
        - https://github.com/1in9e/icp-domains
        - https://github.com/wongzeon/ICP-Checker

    :param domain: str eg: baidu.com
    :return:
    {
      "info": {
        "time": "2023-07-18 11:04:32",
        "title": "百度",
        "icp": "京ICP证030173号-1",
        "name": "北京百度网讯科技有限公司",
        "nature": "企业"
      },
      "domain": "baidu.com",
      "success": true
    }
    """
    url = 'https://api.vvhan.com/api/icp'
    params = {
        'url': domain
    }
    res = requests.get(url, params)
    return res.json().get('info')


if __name__ == '__main__':
    print(json_util.json_encode(get_icp('baidu.com'), indent=2, ensure_ascii=False))
