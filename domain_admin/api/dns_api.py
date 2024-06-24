# -*- coding: utf-8 -*-
"""
@File    : dns_api.py
@Date    : 2023-07-29
"""
from flask import request, g

from domain_admin.enums.dns_type_enum import DnsTypeEnum
from domain_admin.model.dns_model import DnsModel


def add_dns():
    """
    添加Dns
    :return:
    """
    current_user_id = g.user_id

    dns_type_id = request.json.get('dns_type_id') or DnsTypeEnum.ALIYUN
    name = request.json['name']
    access_key = request.json['access_key']
    secret_key = request.json['secret_key']

    row = DnsModel.create(
        user_id=current_user_id,
        dns_type_id=dns_type_id,
        name=name,
        access_key=access_key,
        secret_key=secret_key,
    )

    return row


def update_dns_by_id():
    """
    更新Dns
    :return:
    """
    current_user_id = g.user_id

    dns_type_id = request.json.get('dns_type_id') or DnsTypeEnum.ALIYUN
    dns_id = request.json['dns_id']
    name = request.json['name']
    access_key = request.json['access_key']
    secret_key = request.json['secret_key']

    DnsModel.update(
        dns_type_id=dns_type_id,
        name=name,
        access_key=access_key,
        secret_key=secret_key,
    ).where(
        DnsModel.id == dns_id
    ).execute()


def get_dns_by_id():
    """
    获取Dns
    :return:
    """
    dns_id = request.json['dns_id']

    return DnsModel.get_by_id(dns_id)


def delete_dns_by_id():
    """
    移除Dns
    :return:
    """
    dns_id = request.json['dns_id']

    return DnsModel.delete_by_id(dns_id)


def get_dns_list():
    """
    Dns列表
    :return:
    """

    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    keyword = request.json.get('keyword')
    dns_type_id = request.json.get('dns_type_id')

    query = DnsModel.select().where(
        DnsModel.user_id == current_user_id
    )

    if keyword:
        query = query.where(DnsModel.name.contains(keyword))
    if dns_type_id:
        query = query.where(DnsModel.dns_type_id == dns_type_id)

    total = query.count()

    rows = query.order_by(
        DnsModel.create_time.desc(),
        DnsModel.id.desc()
    )

    return {
        'list': rows,
        'total': total,
    }

