# -*- coding: utf-8 -*-
from flask import request

from domain_admin.model import DomainModel


def add_domain():
    """
    添加域名
    :return:
    """
    domain = request.json.get('domain')
    alias = request.json.get('alias', '')

    DomainModel.create(
        domain=domain,
        alias=alias
    )


def update_domain_by_id():
    pass


def delete_domain_by_id():
    pass


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
    domain_id = request.json.get('id')

    return DomainModel.get_by_id(domain_id)
