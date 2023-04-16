# -*- coding: utf-8 -*-
"""
@File    : whois_util.py
@Date    : 2023-03-24
"""
import json
from copy import deepcopy
from datetime import datetime

from dateutil import parser

from domain_admin.log import logger
from domain_admin.utils import json_util
from domain_admin.utils.whois_util.config import CUSTOM_WHOIS_CONFIGS, DEFAULT_WHOIS_CONFIG
from domain_admin.utils.whois_util.util import parse_whois_raw, get_whois_raw, load_whois_servers

WHOIS_CONFIGS = None


def parse_time(time_str, time_format=None):
    """
    解析时间字符串为时间对象
    :param time_str:
    :param time_format:
    :return:
    """
    if time_format:
        time_parsed = datetime.strptime(time_str, time_format)
    else:
        time_parsed = parser.parse(time_str).replace(tzinfo=None)

    return time_parsed


def load_whois_servers_config():
    """
    加载whois_servers配置
    :return:
    """
    whois_servers = load_whois_servers()

    config = {}

    for root, server in whois_servers.items():

        if root in CUSTOM_WHOIS_CONFIGS:
            # 自定义配置优先
            config[root] = CUSTOM_WHOIS_CONFIGS[root]
        else:
            # 通用配置
            server_config = deepcopy(DEFAULT_WHOIS_CONFIG)
            server_config['whois_server'] = server
            config[root] = server_config

    return config


def get_whois_config(domain: str) -> [str, None]:
    """
    获取域名信息所在服务器
    :param domain:
    :return:
    """
    global WHOIS_CONFIGS

    logger.debug('get_whois_config %s', domain)
    root = domain.split('.')[-1]

    if WHOIS_CONFIGS is None:
        WHOIS_CONFIGS = load_whois_servers_config()

    if root in WHOIS_CONFIGS:
        return WHOIS_CONFIGS.get(root)
    else:
        # TODO：从根服务器查询域名信息服务器
        raise Exception(f'not support {root}')


def get_domain_whois(domain):
    logger.debug('get_domain_whois %s', domain)

    whois_config = get_whois_config(domain)

    whois_server = whois_config['whois_server']
    # error = whois_config['error']
    registry_time = whois_config['registry_time']
    expire_time = whois_config['expire_time']
    registry_time_format = whois_config.get('registry_time_format')
    expire_time_format = whois_config.get('expire_time_format')

    raw_data = get_whois_raw(domain, whois_server, timeout=10)
    logger.debug(raw_data)

    # if error in raw_data:
    #     return None

    data = parse_whois_raw(raw_data)
    logger.debug(json.dumps(data, indent=2))

    start_time = data.get(registry_time)
    expire_time = data.get(expire_time)

    if start_time:
        start_time = parse_time(start_time, registry_time_format)

    if expire_time:
        expire_time = parse_time(expire_time, expire_time_format)

    if start_time and expire_time:
        return {
            'start_time': start_time,
            'expire_time': expire_time,
        }
    else:
        return None


def get_domain_info(domain: str):
    """
    获取域名信息
    :param domain:
    :return:
    """
    # 处理带端口号的域名
    # if ':' in domain:
    #     domain = domain.split(":")[0]

    res = get_domain_whois(domain)

    # 解决二级域名查询失败的问题
    # if not res:
    #     domain = ".".join(domain.split(".")[1:])
    #     res = get_domain_whois(domain)

    logger.debug(json_util.json_encode(res, indent=2))

    return res
