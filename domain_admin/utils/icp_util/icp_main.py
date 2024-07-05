# -*- coding: utf-8 -*-
"""
@File    : icp_util.py
@Date    : 2023-06-30
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.utils import json_util
from domain_admin.utils.icp_util.icp_api import uutool_icp_api, uomg_icp_api


def get_icp(domain):
    """
    备案查询网站：
    https://www.beianx.cn/
    https://beian.miit.gov.cn/#/Integrated/index
    :param domain:
    :return: ICPItem
    """
    # 第三方接口
    return uomg_icp_api.get_icp_from_uomg(domain)


if __name__ == '__main__':
    # print(json_util.json_encode(get_icp('baidu.com'), indent=2, ensure_ascii=False))
    print(json_util.json_encode(get_icp('qq.com'), indent=2, ensure_ascii=False))
