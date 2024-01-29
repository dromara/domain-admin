# -*- coding: utf-8 -*-
"""
@File    : vvhan_icp_api.py
@Date    : 2024-01-29
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import requests

from domain_admin.log import logger
from domain_admin.utils.icp_util.icp_item import ICPItem


def get_icp_from_vvhan(domain):
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

    logger.debug(res.text)

    info = res.json().get('info')

    item = ICPItem()
    item.name = info.get('name', '')
    item.icp = info.get('icp', '')

    return item
