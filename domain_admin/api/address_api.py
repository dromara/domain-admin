# -*- coding: utf-8 -*-
"""
address_api.py
"""

from __future__ import print_function, unicode_literals, absolute_import, division
from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.model.address_model import AddressModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.service import domain_service
from domain_admin.utils.flask_ext.app_exception import AppException


def get_address_list_by_domain_id():
    """
    通过域名获取关联的主机地址列表
    :return:
    @since v1.3.1
    """

    current_user_id = g.user_id

    domain_id = request.json['domain_id']
    page = request.json.get('page', 1)
    size = request.json.get('size', 10)

    query = AddressModel.select().where(
        AddressModel.domain_id == domain_id,
    )

    total = query.count()
    lst = []

    if total > 0:
        rows = query.order_by(
            AddressModel.ssl_expire_days,
            AddressModel.id,
        ).paginate(page, size)

        lst = list(map(lambda m: model_to_dict(
            model=m,
            extra_attrs=[
                'ssl_start_date',
                'ssl_expire_date',
                'real_time_ssl_expire_days',
                'update_time_label',
            ]
        ), rows))

    return {
        "list": lst,
        "total": total
    }


def add_address():
    """
    添加主机地址
    :return:
    @since v1.3.1
    """

    current_user_id = g.user_id

    domain_id = request.json['domain_id']
    host = request.json['host']
    ssl_start_time = request.json.get('ssl_start_time')
    ssl_expire_time = request.json.get('ssl_expire_time')
    # ssl_auto_update = request.json.get('ssl_auto_update', True)
    # ssl_expire_monitor = request.json.get('ssl_expire_monitor', True)

    domain_row = DomainModel.get_by_id(domain_id)

    data = {
        'domain_id': domain_id,
        'host': host,
    }

    if not domain_row.auto_update:
        data['ssl_start_time'] = ssl_start_time
        data['ssl_expire_time'] = ssl_expire_time

    address_row = AddressModel.create(**data)

    if domain_row.auto_update:
        domain_service.update_address_row_info_with_sync_domain_row(address_row.id)
    else:
        domain_service.sync_address_info_to_domain_info(domain_row)


def delete_address_by_id():
    """
    删除主机地址
    :return:
    @since v1.3.1
    """

    current_user_id = g.user_id

    address_id = request.json['address_id']

    # update to cert
    address_row = AddressModel.get_by_id(address_id)

    AddressModel.delete().where(
        AddressModel.id == address_id
    ).execute()

    domain_row = DomainModel.get_by_id(address_row.domain_id)
    domain_service.sync_address_info_to_domain_info(domain_row)


def delete_address_by_ids():
    """
    批量删除主机地址
    :return:
    @since v1.4.4
    """

    current_user_id = g.user_id

    address_ids = request.json['address_ids']

    # update to cert
    address_rows = AddressModel.select(AddressModel.domain_id).where(
        AddressModel.id.in_(address_ids)
    )

    AddressModel.delete().where(
        AddressModel.id.in_(address_ids)
    ).execute()

    domain_ids = [row.domain_id for row in address_rows]

    domain_rows = DomainModel.select().where(
        DomainModel.id.in_(domain_ids)
    )

    for domain_row in domain_rows:
        domain_service.sync_address_info_to_domain_info(domain_row)


def get_address_by_id():
    """
    获取主机地址
    :return:
    @since v1.3.1
    """

    current_user_id = g.user_id

    address_id = request.json['address_id']

    return AddressModel.get_by_id(address_id)


def update_address_by_id():
    """
    更新主机地址
    :return:
    @since v1.3.1
    """

    current_user_id = g.user_id

    address_id = request.json['address_id']
    host = request.json['host']
    ssl_start_time = request.json.get('ssl_start_time')
    ssl_expire_time = request.json.get('ssl_expire_time')
    # ssl_auto_update = request.json.get('ssl_auto_update', True)
    # ssl_expire_monitor = request.json.get('ssl_expire_monitor', True)

    address_row = AddressModel.get_by_id(address_id)
    domain_row = DomainModel.get_by_id(address_row.domain_id)

    data = {
        'host': host
    }

    if not domain_row.auto_update:
        data['ssl_start_time'] = ssl_start_time
        data['ssl_expire_time'] = ssl_expire_time

    AddressModel.update(data).where(
        AddressModel.id == address_id
    ).execute()

    if domain_row.auto_update:
        domain_service.update_address_row_info_with_sync_domain_row(address_id)
    else:
        domain_service.sync_address_info_to_domain_info(domain_row)


def update_address_list_info_by_domain_id():
    """
    更新主机地址信息
    :return:
    @since v1.3.1
    """

    current_user_id = g.user_id

    domain_id = request.json['domain_id']

    domain_row = DomainModel.get_by_id(domain_id)

    err = domain_service.update_domain_row(domain_row)

    if err:
        raise AppException(err)


def update_address_row_info_by_id():
    """
    更新主机地址信息
    :return:
    @since v1.3.1
    """

    current_user_id = g.user_id

    address_id = request.json['address_id']

    domain_service.update_address_row_info_with_sync_domain_row(address_id)
