# -*- coding: utf-8 -*-
"""
@File    : qq_icp_api.py
@Date    : 2024-01-29
@Author  : Peng Shiyu
"""

from __future__ import print_function, unicode_literals, absolute_import, division

import json
import re

import requests

from domain_admin.log import logger
from domain_admin.utils.icp_util.icp_item import ICPItem


def get_icp_from_qq(domain):
    """
    接口由网友 @因为遇见你 提供
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
        data = json.loads(data)

        code = data.get('reCode')

        if code != 0:
            raise Exception(data.get('data'))

        results = data.get('data').get('results')

        item = ICPItem()
        item.name = results.get('Orgnization', '')
        item.icp = results.get('ICPSerial', '')
        return item


if __name__ == '__main__':
    print(get_icp_from_qq('qq.com'))
