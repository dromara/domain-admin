# -*- coding: utf-8 -*-
from flask import request

from domain_admin.model import DomainModel
from domain_admin.utils.datetime_util import get_datetime


def add_domain():
    """
    添加域名
    :return:
    """
    domain = request.json.get('domain')
    alias = request.json.get('alias', '')
    group_id = request.json.get('group_id', 0)

    DomainModel.create(
        domain=domain,
        alias=alias,
        group_id=group_id
    )


def update_domain_by_id():
    """
    更新数据
    :return:
    """
    domain_id = request.json.get('id')
    domain = request.json.get('domain')
    alias = request.json.get('alias', '')
    group_id = request.json.get('group_id', 0)

    DomainModel.update(
        domain=domain,
        alias=alias,
        group_id=group_id,
        update_time=get_datetime()
    ).where(
        DomainModel.id == domain_id
    ).execute()


def delete_domain_by_id():
    """
    删除
    :return:
    """
    domain_id = request.json.get('id')

    DomainModel.delete_by_id(domain_id)


def get_domain_list():
    """
    获取域名列表
    :return:
    """
    page = request.json.get('page', 1)
    size = request.json.get('size', 10)

    lst = DomainModel.select().order_by(
        DomainModel.update_time.desc()
    ).paginate(page, size)

    total = DomainModel.select().count()

    return {
        'list': lst,
        'total': total
    }


def get_domain_by_id():
    """
    获取
    :return:
    """
    domain_id = request.json.get('id')

    return DomainModel.get_by_id(domain_id)
