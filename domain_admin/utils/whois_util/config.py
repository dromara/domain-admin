# -*- coding: utf-8 -*-
"""
@File    : config.py
@Date    : 2023-03-25
"""

# 根服务器地址
ROOT_SERVER = 'whois.iana.org'

# https://www.nirsoft.net/whois-servers.txt
# https://www.iana.org/domains/root/db
WHOIS_CONFIGS = {
    'cn': {
        'whois_server': 'whois.cnnic.cn',
        'error': 'Invalid parameter',
        'registry_time': 'Registration Time',
        'expire_time': 'Expiration Time',
    },

    'com': {
        'whois_server': 'whois.verisign-grs.com',
        'error': 'No match',
        'registry_time': 'Creation Date',
        'expire_time': 'Registry Expiry Date'
    }
}
