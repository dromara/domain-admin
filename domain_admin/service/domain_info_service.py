# -*- coding: utf-8 -*-
"""
domain_info_service.py
"""

from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.utils import whois_util, datetime_util


def update_domain_info_row(row: DomainInfoModel) -> [str, None]:
    """
    更新一行数据
    :param row:
    :return:
    """
    domain_whois = None

    try:
        domain_whois = whois_util.get_domain_info(row.domain)
    except Exception as e:
        pass

    update_row = DomainInfoModel()

    if domain_whois:
        update_row.domain_start_time = domain_whois['start_time']
        update_row.domain_expire_time = domain_whois['expire_time']

    DomainInfoModel.update(
        domain_start_time=update_row.domain_start_time,
        domain_expire_time=update_row.domain_expire_time,
        domain_expire_days=update_row.real_domain_expire_days,
        update_time=datetime_util.get_datetime()
    ).where(
        DomainInfoModel.id == row.id
    ).execute()
