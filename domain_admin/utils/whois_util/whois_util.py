# -*- coding: utf-8 -*-
"""
@File    : whois_util.py
@Date    : 2023-03-24
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import json
import re
from copy import deepcopy
from datetime import datetime

from dateutil import parser

from domain_admin.log import logger
from domain_admin.utils import json_util, domain_util
from domain_admin.utils.whois_util.config import (
    CUSTOM_WHOIS_CONFIGS,
    DEFAULT_WHOIS_CONFIG,
    ROOT_SERVER,
    REGISTRAR_CONFIG_MAP
)
from domain_admin.utils.whois_util.util import parse_whois_raw, get_whois_raw, load_whois_servers

WHOIS_CONFIGS = None


class DomainInfo(object):
    start_time = None
    expire_time = None


def resolve_domain(domain):
    """
    域名转换
    :param domain: str
    :return: str
    """
    # 解析出域名和顶级后缀
    if domain_util.is_ipv4(domain):
        return domain
    else:
        root_domain = domain_util.get_root_domain(domain)
        return domain_util.encode_hostname(root_domain)


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

    # 通用配置
    for root, server in whois_servers.items():
        server_config = deepcopy(DEFAULT_WHOIS_CONFIG)
        server_config['whois_server'] = server
        config[domain_util.encode_hostname(root)] = server_config

    # 自定义配置优先
    for key, value in CUSTOM_WHOIS_CONFIGS.items():
        encode_key = domain_util.encode_hostname(key)
        default_config = config.get(encode_key, deepcopy(DEFAULT_WHOIS_CONFIG))
        default_config.update(value)
        config[encode_key] = default_config

        # 合并配置
    # logger.debug(config)
    return config


def get_whois_config(domain):
    """
    获取域名信息所在服务器
    :param domain: str
    :return: [str, None]
    """
    global WHOIS_CONFIGS

    # logger.debug('get_whois_config %s', domain)
    root = domain.split('.')[-1]

    if WHOIS_CONFIGS is None:
        WHOIS_CONFIGS = load_whois_servers_config()

    if root in WHOIS_CONFIGS:
        return WHOIS_CONFIGS.get(root)
    else:
        # 从根服务器查询域名信息服务器
        domain_whois_server = get_domain_whois_server_from_root(domain)
        if domain_whois_server:
            server_config = deepcopy(DEFAULT_WHOIS_CONFIG)
            server_config['whois_server'] = domain_whois_server
            return server_config
        else:
            raise Exception('not support {}'.format(root))


def get_domain_whois_server_from_root(domain):
    """
    从根服务器获取域名的查询服务器
    :param domain:
    :return:
    """
    raw_data = get_whois_raw(domain, ROOT_SERVER, timeout=10)
    logger.info(raw_data)

    result = re.findall("refer:(.*)", raw_data)
    if result and len(result) > 0:
        return result[0].strip()


def get_domain_raw_whois(domain):
    whois_config = get_whois_config(domain)

    whois_server = whois_config['whois_server']

    raw_data = get_whois_raw(domain, whois_server, timeout=10)
    logger.debug(raw_data)
    return raw_data


def handle_url(url):
    """
    处理不规范的url
    :param url:
    :return:
    """
    if url.startswith('http://'):
        return url
    elif url.startswith('https://'):
        return url
    else:
        return 'http://' + url


def get_domain_whois(domain):
    logger.debug('get_domain_whois %s', domain)

    raw_data = get_domain_raw_whois(domain)

    data = parse_whois_raw(raw_data)
    logger.debug(json.dumps(data, indent=2, ensure_ascii=False))

    whois_config = get_whois_config(domain)
    logger.debug('whois_config', whois_config)

    whois_server = whois_config['whois_server']
    # error = whois_config['error']
    registry_time = whois_config['registry_time']
    expire_time = whois_config['expire_time']
    registry_time_format = whois_config.get('registry_time_format')
    expire_time_format = whois_config.get('expire_time_format')
    registrar_key = whois_config.get('registrar')
    registrar_url_key = whois_config.get('registrar_url')

    start_time = data.get(registry_time)
    expire_time = data.get(expire_time)

    registrar = data.get(registrar_key, '').strip()
    registrar_url = data.get(registrar_url_key, '').strip()

    if start_time:
        start_time = parse_time(start_time, registry_time_format)

    if expire_time:
        expire_time = parse_time(expire_time, expire_time_format)

    # cn域名注册商
    if registrar and not registrar_url:
        registrar_config = REGISTRAR_CONFIG_MAP.get(registrar)
        if registrar_config:
            registrar_url = registrar_config['registrar_url']

    # 修复 https:// http://
    if registrar_url:
        registrar_url = handle_url(registrar_url)

    if start_time and expire_time:
        return {
            'start_time': start_time,
            'registrar': registrar,
            'registrar_url': registrar_url,
            'expire_time': expire_time,
        }
    else:
        return None


def get_domain_info(domain):
    """
    获取域名信息
    :param domain: str
    :return:
    """
    # 处理带端口号的域名
    domain = resolve_domain(domain)
    logger.debug("resolve_domain: %s", domain)

    res = get_domain_whois(domain)

    logger.debug(json_util.json_encode(res, indent=2, ensure_ascii=False))

    return res


if __name__ == '__main__':
    ret = get_domain_info('baidu.com')
    print(ret)
