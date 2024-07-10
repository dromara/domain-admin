# -*- coding: utf-8 -*-
"""
@File    : uomg_icp_api.py
@Date    : 2024-07-04
"""
import requests

from domain_admin.utils.icp_util.icp_item import ICPItem


def get_icp_from_uomg(domain):
    """
    https://api.uomg.com/doc-icp.html#api
    https://github.com/mouday/domain-admin/issues/112
    {
        "code": 1,
        "domain": "baidu.com",
        "icp": "京ICP证030173号"
    }

    {
        "code": 1,
        "domain": "baidu1.com",
        "icp": "未备案"
    }
    """
    url = 'https://api.uomg.com/api/icp'

    data = {
        "domain": domain
    }

    # 发送GET请求
    response = requests.get(url, params=data, timeout=5)
    print(response.text)
    res = response.json()
    if res.get('icp') == '未备案':
        raise Exception('未备案')

    data = res

    item = ICPItem()
    item.name = data.get('')
    item.icp = data.get('icp')

    return item


if __name__ == '__main__':
    print(get_icp_from_uomg('baidu.com').to_dict())
