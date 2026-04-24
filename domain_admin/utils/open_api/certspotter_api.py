# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

import requests

from domain_admin.log import logger

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'


def search(domain, include_subdomains=True):
    """
    查询 Cert Spotter 证书签发记录
    :param domain: str
    :param include_subdomains: bool
    :return: list
    """
    url = 'https://api.certspotter.com/v1/issuances'

    params = {
        'domain': domain,
        'include_subdomains': 'true' if include_subdomains else 'false',
        'expand': 'dns_names',
    }

    headers = {
        'User-Agent': USER_AGENT
    }

    try:
        req = requests.get(url=url, params=params, headers=headers, timeout=8)
    except Exception:
        logger.error('certspotter request failed: %s', domain)
        return []

    if not req.ok:
        logger.warn('certspotter request not ok: status_code=%s', req.status_code)
        return []

    try:
        return req.json()
    except ValueError:
        logger.warn('certspotter response is not json, status_code=%s', req.status_code)
        return []
