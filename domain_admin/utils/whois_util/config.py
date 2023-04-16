# -*- coding: utf-8 -*-
"""
@File    : config.py
@Date    : 2023-03-25
"""

# 根服务器地址
ROOT_SERVER = 'whois.iana.org'

# 默认的配置，适用于大部分域名查询
DEFAULT_WHOIS_CONFIG = {
    'whois_server': '',  # whois查询服务器
    # 'error': 'No match',                   # 错误信息
    'registry_time': 'Creation Date',  # 注册时间
    'expire_time': 'Registry Expiry Date'  # 过期时间
}

# https://www.nirsoft.net/whois-servers.txt
# https://www.iana.org/domains/root/db

# 自定义配置
CUSTOM_WHOIS_CONFIGS = {
    'cn': {
        'whois_server': 'whois.cnnic.cn',
        'registry_time': 'Registration Time',
        'expire_time': 'Expiration Time',
    },
    'hk': {
        'whois_server': 'whois.hkirc.hk',
        'registry_time': 'Domain Name Commencement Date',
        "registry_time_format": '%d-%m-%Y',
        'expire_time': 'Expiry Date',
        "expire_time_format": '%d-%m-%Y',
    }
}
