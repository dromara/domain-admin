# -*- coding: utf-8 -*-
"""
@File    : domain_icp_service.py
@Date    : 2024-01-31
@Author  : Peng Shiyu
"""
import traceback
from datetime import datetime, timedelta

from domain_admin.model.domain_icp_model import DomainIcpModel
from domain_admin.utils import icp_util
from domain_admin.utils.icp_util.icp_item import ICPItem

from domain_admin.log import logger


def get_domain_icp(domain):
    """
    获取域名icp数据
    :param domain:
    :return: ICPItem / None
    """

    domain_icp_row = DomainIcpModel.select().where(
        DomainIcpModel.domain == domain,
    ).first()

    if domain_icp_row and not domain_icp_row.is_expired:
        item = ICPItem()
        item.domain = domain
        item.icp = domain_icp_row.icp_licence
        item.name = domain_icp_row.icp_company
    else:
        item = None

        try:
            item = icp_util.get_icp(domain)
        except Exception as e:
            logger.debug(traceback.format_exc())

        if item:
            data = {
                'domain': domain,
                'icp_company': item.name,
                'icp_licence': item.icp,
                # 缓存有效期 23小时
                'expire_time': datetime.now() + timedelta(hours=23)
            }

            if domain_icp_row:
                DomainIcpModel.set_by_id(domain_icp_row.id, data)
            else:
                DomainIcpModel.create(**data)

    return item
