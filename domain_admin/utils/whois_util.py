# -*- coding: utf-8 -*-
"""
@File    : whois_util.py
@Date    : 2023-03-24
"""
import requests
import whois


def get_domain_info_by_whois(domain):
    url = 'https://www.whois.com/whois/' + domain

    res = requests.get(url)
    if res.ok:
        print(res.content)


def get_domain_info(domain: str):
    """
    获取域名信息
    :param domain:
    :return:
    """

    domain_info = whois.query(domain, ignore_returncode=True)

    return {
        'start_time': domain_info.creation_date,
        'expire_time': domain_info.expiration_date
    }
