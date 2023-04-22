# -*- coding: utf-8 -*-
"""
@File    : cache_domain_info_service.py
@Date    : 2023-04-22
"""
from datetime import datetime, timedelta

from domain_admin.model.cache_domain_info_model import CacheDomainInfoModel
from domain_admin.utils import domain_util
from domain_admin.utils.whois_util import whois_util


def get_domain_info(domain: str) -> CacheDomainInfoModel:
    """
    加一个缓存获取域名信息
    :param domain:
    :return:
    """
    root_domain = domain_util.get_root_domain(domain)

    row = CacheDomainInfoModel.select().where(
        CacheDomainInfoModel.domain == root_domain
    ).get_or_none()

    # 不存在或者已过期，重新获取
    if not row or row.is_expired is True:
        domain_whois = whois_util.get_domain_whois(root_domain)

        if domain_whois is None:
            raise Exception("域名信息获取失败")

        row = CacheDomainInfoModel.create(
            domain=root_domain,
            domain_start_time=domain_whois['start_time'],
            domain_expire_time=domain_whois['expire_time'],
            expire_time=domain_whois['expire_time'] - timedelta(minutes=3)
        )

    return row
