# -*- coding: utf-8 -*-
"""
@File    : icp_util.py
@Date    : 2023-06-30
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import json
import re

import requests

from domain_admin.log import logger
from domain_admin.utils import json_util


class ICPItem(object):
    name = ''
    icp = ''

    def to_dict(self):
        return {
            'name': self.name,
            'icp': self.icp,
        }


def get_icp_from_qq(domain):
    """
    接口由网友提供
    :param domain:
    :return:

    ({
        "data": {
            "retcode": 0,
            "results": {
                "url": "baidu.com",
                "whitetype": 3,
                "WordingTitle": "",
                "Wording": "",
                "detect_time": "1657588645",
                "eviltype": "0",
                "certify": 0,
                "isDomainICPOk": 1,
                "Orgnization": "北京百度网讯科技有限公司",
                "ICPSerial": "京ICP证030173号-1"
            }
        },
        "reCode": 0
    })
    """
    url = 'https://cgi.urlsec.qq.com/index.php'

    params = {
        'm': 'check',
        'a': 'check',
        'url': domain
    }

    headers = {
        'Referer': 'https://guanjia.qq.com'
    }

    res = requests.get(url, params, headers=headers)

    logger.debug(res.text)

    ret = re.match("\((?P<data>.*)\)", res.text)

    if ret:
        data = ret.groupdict().get('data')
        results = json.loads(data).get('data').get('results')

        item = ICPItem()
        item.name = results.get('Orgnization', '')
        item.icp = results.get('ICPSerial', '')
        return item


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


def get_icp(domain):
    return get_icp_from_qq(domain).to_dict()


if __name__ == '__main__':
    # print(json_util.json_encode(get_icp('baidu.com'), indent=2, ensure_ascii=False))
    print(json_util.json_encode(get_icp_from_qq('baidu.com').to_dict(), indent=2, ensure_ascii=False))
