# -*- coding: utf-8 -*-
"""
@File    : config.py
@Date    : 2023-03-25
"""
from __future__ import print_function, unicode_literals, absolute_import, division

from os import path

from domain_admin.config import TEMP_DIR

DEFAULT_WHOIS_SERVERS_PATH = path.join(path.dirname(__file__), 'whois-servers.txt')
TEMP_WHOIS_SERVERS_PATH = path.join(TEMP_DIR, 'whois-servers.txt')

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
        # 'whois_server': 'whois.twnic.net',
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
    },
    'im': {
        'expire_time': 'Expiry Date',
        'expire_time_format': '%d/%m/%Y %H:%M:%S',
    },
    'kr': {
        'whois_server': 'whois.kr',
        'registry_time': 'Registered Date',
        "registry_time_format": '%Y. %m. %d.',
        'expire_time': 'Expiration Date',
        "expire_time_format": '%Y. %m. %d.',
    },
    'lt': {
        # 'whois_server': 'whois.lt',
        'registry_time': 'Registered',
        'expire_time': 'Expires',
    },
    'uk': {
        # 'whois_server': 'whois.lt',
        'registry_time': 'Registered on',
        'expire_time': 'Expiry date',
    },

    # 多级域名配置 - 印度域名
    'co.in': {
        'whois_server': 'whois.nixiregistry.in',
        'registry_time': 'Creation Date',
        'expire_time': 'Registry Expiry Date',
    },
    'net.in': {
        'whois_server': 'whois.nixiregistry.in',
        'registry_time': 'Creation Date',
        'expire_time': 'Registry Expiry Date',
    },
    'org.in': {
        'whois_server': 'whois.nixiregistry.in',
        'registry_time': 'Creation Date',
        'expire_time': 'Registry Expiry Date',
    },
    'com.in': {
        'whois_server': 'whois.nixiregistry.in',
        'registry_time': 'Creation Date',
        'expire_time': 'Registry Expiry Date',
    },

    # 多级域名配置 - 英国域名
    'co.uk': {
        'whois_server': 'whois.nic.uk',
        'registry_time': 'Registered on',
        'expire_time': 'Expiry date',
    },
    'org.uk': {
        'whois_server': 'whois.nic.uk',
        'registry_time': 'Registered on',
        'expire_time': 'Expiry date',
    },
    'net.uk': {
        'whois_server': 'whois.nic.uk',
        'registry_time': 'Registered on',
        'expire_time': 'Expiry date',
    },

    # 多级域名配置 - 澳大利亚域名
    'com.au': {
        'whois_server': 'whois.auda.org.au',
        'registry_time': 'Last Modified',
        'expire_time': 'Status Reason',
    },
    'net.au': {
        'whois_server': 'whois.auda.org.au',
        'registry_time': 'Last Modified',
        'expire_time': 'Status Reason',
    },
    'org.au': {
        'whois_server': 'whois.auda.org.au',
        'registry_time': 'Last Modified',
        'expire_time': 'Status Reason',
    },

    # 多级域名配置 - 新西兰域名
    'co.nz': {
        'whois_server': 'whois.irs.net.nz',
        'registry_time': 'Domain name registered',
        'expire_time': 'Registrar expires',
    },
    'org.nz': {
        'whois_server': 'whois.irs.net.nz',
        'registry_time': 'Domain name registered',
        'expire_time': 'Registrar expires',
    },

    # 多级域名配置 - 南非域名
    'co.za': {
        'whois_server': 'whois.registry.net.za',
        'registry_time': 'Creation Date',
        'expire_time': 'Expiration Date',
    },
    'org.za': {
        'whois_server': 'whois.registry.net.za',
        'registry_time': 'Creation Date',
        'expire_time': 'Expiration Date',
    },

    # 多级域名配置 - 新加坡域名
    'com.sg': {
        'whois_server': 'whois.sgnic.sg',
        'registry_time': 'Creation Date',
        'expire_time': 'Expiration Date',
    },
    'net.sg': {
        'whois_server': 'whois.sgnic.sg',
        'registry_time': 'Creation Date',
        'expire_time': 'Expiration Date',
    },

    # 多级域名配置 - 马来西亚域名
    'com.my': {
        'whois_server': 'whois.mynic.my',
        'registry_time': 'Created Date',
        'expire_time': 'Expired Date',
    },
    'net.my': {
        'whois_server': 'whois.mynic.my',
        'registry_time': 'Created Date',
        'expire_time': 'Expired Date',
    },

    # 多级域名配置 - 香港域名
    'com.hk': {
        'whois_server': 'whois.hkirc.hk',
        'registry_time': 'Domain Name Commencement Date',
        'expire_time': 'Expiry Date',
        'expire_time_format': '%d-%m-%Y',
    },
    'net.hk': {
        'whois_server': 'whois.hkirc.hk',
        'registry_time': 'Domain Name Commencement Date',
        'expire_time': 'Expiry Date',
        'expire_time_format': '%d-%m-%Y',
    },

    # 多级域名配置 - 台湾域名
    'com.tw': {
        'whois_server': 'whois.twnic.net.tw',
        'registry_time': 'Record created',
        'expire_time': 'Record expires',
    },
    'net.tw': {
        'whois_server': 'whois.twnic.net.tw',
        'registry_time': 'Record created',
        'expire_time': 'Record expires',
    },
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
