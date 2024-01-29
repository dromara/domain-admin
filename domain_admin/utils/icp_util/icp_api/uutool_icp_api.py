# -*- coding: utf-8 -*-
"""
@File    : uutool_icp_api.py
@Date    : 2024-01-29
@Author  : Peng Shiyu
"""

import requests

from domain_admin.utils.icp_util.icp_item import ICPItem


def get_icp_from_uutool(domain):
    """
    https://uutool.cn/icp/

    {
        "status":1,
        "data":{
            "domain":"baidu.com",
            "is_icp":1,
            "icp_org":"北京百度网讯科技有限公司",
            "icp_no":"京ICP证030173号-1"
        },
        "req_id":"9e0dd2773b3a84244406"
    }

    :param domain:
    :return:


    """
    url = 'https://api.uutool.cn/beian/icp/'

    data = {
        "domain": domain
    }

    # 发送GET请求
    response = requests.post(url, data=data)
    # print(response.text)

    res = response.json()
    if res.get('status') != 1:
        raise Exception(res.get('error'))

    data = res.get('data')

    item = ICPItem()
    item.name = data.get('icp_org')
    item.icp = data.get('icp_no')

    return item


if __name__ == '__main__':
    print(get_icp_from_uutool('baodu.com').to_dict())
