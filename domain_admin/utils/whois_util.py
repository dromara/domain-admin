# -*- coding: utf-8 -*-
"""
@File    : whois_util.py
@Date    : 2023-03-24
"""
import requests
from parsel import Selector
from dateutil import parser


def get_domain_info_by_whois(domain):
    url = 'https://www.whois.com/whois/' + domain

    data = {}

    res = requests.get(url, timeout=5)
    if res.ok:
        sel = Selector(res.text)
        text = sel.css('#registrarData::text').get("")
        rows = text.split("\n")

        for row in rows:
            row_split = row.split(': ')
            if len(row_split) == 2:
                label, value = row_split
                data[label] = value

    return data


def get_domain_info(domain: str):
    """
    获取域名信息
    :param domain:
    :return:
    """

    res = get_domain_info_by_whois(domain)

    start_time = res.get('Creation Date')
    expire_time = res.get('Registrar Registration Expiration Date')

    if start_time:
        start_time = parser.parse(start_time)

    if expire_time:
        expire_time = parser.parse(expire_time)

    return {
        'start_time': start_time,
        'expire_time': expire_time
    }
