# -*- coding: utf-8 -*-
"""
@File    : config.py
@Date    : 2023-03-25
"""
from __future__ import print_function, unicode_literals, absolute_import, division
# 根服务器地址
ROOT_SERVER = 'whois.iana.org'

# 默认的配置，适用于大部分域名查询
DEFAULT_WHOIS_CONFIG = {
    'whois_server': '',  # whois查询服务器
    # 'error': 'No match',                   # 错误信息
    'registry_time': 'Creation Date',  # 注册时间
    'expire_time': 'Registry Expiry Date',  # 过期时间
    'registrar': 'Registrar',  # 注册商
    'registrar_url': 'Registrar URL',  # 注册商url
}

# https://www.nirsoft.net/whois-servers.txt
# https://www.iana.org/domains/root/db

# 自定义配置
CUSTOM_WHOIS_CONFIGS = {
    'cn': {
        'whois_server': 'whois.cnnic.cn',
        'registry_time': 'Registration Time',
        'expire_time': 'Expiration Time',
        'registrar': 'Sponsoring Registrar',
    },
    'hk': {
        'whois_server': 'whois.hkirc.hk',
        'registry_time': 'Domain Name Commencement Date',
        "registry_time_format": '%d-%m-%Y',
        'expire_time': 'Expiry Date',
        "expire_time_format": '%d-%m-%Y',
    },
    'sg': {
        'whois_server': 'whois.sgnic.sg',
        'registry_time': 'Creation Date',
        # "registry_time_format": '%d-%m-%Y',
        'expire_time': 'Expiration Date',
        # "expire_time_format": '%d-%m-%Y',
    },
    'jp': {
        'whois_server': 'whois.jprs.jp',
        'registry_time': '[登録年月日]',
        "registry_time_format": '%Y/%m/%d',
        'expire_time': '[有効期限]',
        "expire_time_format": '%Y/%m/%d',
    },

    '中国': {
        'whois_server': 'cwhois.cnnic.cn',
        'registry_time': 'Registration Time',
        'expire_time': 'Expiration Time',
    },
    'tw': {
        'whois_server': 'whois.twnic.net',
        'registry_time': 'Record created',
        "registry_time_format": '%Y-%m-%d %H:%M:%S (UTC+8)',
        'expire_time': 'Record expires',
        "expire_time_format": '%Y-%m-%d %H:%M:%S (UTC+8)',
    },
    'ws': {
        'registry_time': 'Creation Date',
        'expire_time': 'Registrar Registration Expiration Date',
    },

    # 网页查询：https://www.whois.cm/
    'cm': {
        'whois_server': 'whois.registrar.cm',
        'registry_time': 'Creation Date',
        'expire_time': 'Registry Expiry Date'
    },
    'by': {
        'whois_server': 'whois.cctld.by',
        'registry_time': 'Creation Date',
        'expire_time': 'Expiration Date',
    }
}

# 国内cn域名注册商
REGISTRAR_CONFIG = [
    {
        'registrar': '厦门易名科技股份有限公司',
        'registrar_url': 'https://www.ename.net/'
    },
    {
        'registrar': '北京中科三方网络技术有限公司',
        'registrar_url': 'https://www.sfn.cn/'
    }
]

# 国内cn域名注册商map
REGISTRAR_CONFIG_MAP = {
    config['registrar']: config
    for config in REGISTRAR_CONFIG
}
