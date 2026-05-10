# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

import requests

from domain_admin.log import logger


def search_domain_certificates(domain, api_key):
    """
    使用 Shodan DNS domain API 查询域名证书索引
    :param domain: str
    :param api_key: str
    :return: list
    """
    if not api_key:
        return []

    url = "https://api.shodan.io/dns/domain/{domain}".format(domain=domain)

    params = {
        'key': api_key
    }

    try:
        req = requests.get(url=url, params=params, timeout=8)
    except Exception:
        logger.error('shodan request failed: %s', domain)
        return []

    if not req.ok:
        if req.status_code == 404:
            return []

        logger.warn('shodan request not ok: status_code=%s', req.status_code)
        return []

    try:
        data = req.json()
    except ValueError:
        logger.warn('shodan response is not json, status_code=%s', req.status_code)
        return []

    return data.get('data', []) if isinstance(data, dict) else []


def get_certificate_by_sha1(sha1, api_key):
    """
    通过证书指纹查询证书详情
    :param sha1: str
    :param api_key: str
    :return: dict
    """
    if not api_key or not sha1:
        return {}

    url = "https://api.shodan.io/shodan/host/search"

    params = {
        'key': api_key,
        'query': 'ssl.cert.fingerprint:{sha1}'.format(sha1=sha1),
        'facets': '',
        'minify': 'false'
    }

    try:
        req = requests.get(url=url, params=params, timeout=8)
    except Exception:
        logger.error('shodan cert detail request failed: %s', sha1)
        return {}

    if not req.ok:
        logger.warn('shodan cert detail request not ok: status_code=%s', req.status_code)
        return {}

    try:
        data = req.json()
    except ValueError:
        logger.warn('shodan cert detail response is not json, status_code=%s', req.status_code)
        return {}

    matches = data.get('matches') if isinstance(data, dict) else None
    if not matches:
        return {}

    match = matches[0] if isinstance(matches, list) else {}
    ssl_data = match.get('ssl') if isinstance(match, dict) else {}
    cert = ssl_data.get('cert') if isinstance(ssl_data, dict) else {}

    return cert if isinstance(cert, dict) else {}
