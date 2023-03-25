# -*- coding: utf-8 -*-
"""
@File    : whois_util.py
@Date    : 2023-03-24
"""

from dateutil import parser

from domain_admin.log import logger
from domain_admin.utils.whois_util.config import WHOIS_CONFIGS
from domain_admin.utils.whois_util.util import parse_whois_raw, get_whois_raw


def get_whois_config(domain: str) -> [str, None]:
    """
    获取域名信息所在服务器
    :param domain:
    :return:
    """
    root = domain.split('.')[-1]

    if root in WHOIS_CONFIGS:
        return WHOIS_CONFIGS.get(root)
    else:
        raise Exception('not support')


def get_domain_whois(domain):
    whois_config = get_whois_config(domain)

    whois_server = whois_config['whois_server']
    error = whois_config['error']
    registry_time = whois_config['registry_time']
    expire_time = whois_config['expire_time']

    raw_data = get_whois_raw(domain, whois_server)
    logger.debug(raw_data)

    if error in raw_data:
        return None

    data = parse_whois_raw(raw_data)
    logger.debug(data)

    start_time = data.get(registry_time)
    expire_time = data.get(expire_time)

    if start_time:
        start_time = parser.parse(start_time).replace(tzinfo=None)
    if expire_time:
        expire_time = parser.parse(expire_time).replace(tzinfo=None)

    return {
        'start_time': start_time,
        'expire_time': expire_time,
    }


def get_domain_info(domain: str):
    """
    获取域名信息
    :param domain:
    :return:
    """
    # 处理带端口号的域名
    if ':' in domain:
        domain = domain.split(":")[0]

    res = get_domain_whois(domain)

    # 解决二级域名查询失败的问题
    if not res:
        domain = ".".join(domain.split(".")[1:])
        res = get_domain_whois(domain)

    logger.debug(res)

    return res
