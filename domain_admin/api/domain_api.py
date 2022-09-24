# -*- coding: utf-8 -*-
from flask import request
from playhouse.shortcuts import model_to_dict

from domain_admin.model import DomainModel
from domain_admin.service.domain_service import update_domain_cert_info
from domain_admin.utils.datetime_util import get_datetime


def add_domain():
    """
    添加域名
    :return:
    """
    domain = request.json.get('domain')
    alias = request.json.get('alias', '')
    group_id = request.json.get('group_id', 0)

    row = DomainModel.create(
        domain=domain,
        alias=alias,
        group_id=group_id
    )

    return {'id': row.id}


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
    group_id = request.json.get('group_id', 0)

    query = DomainModel.select()

    if isinstance(group_id, int):
        query = query.where(DomainModel.group_id == group_id)

    lst = query.order_by(
        DomainModel.update_time.desc()
    ).paginate(page, size)

    total = DomainModel.select().count()

    lst = list(map(lambda m: model_to_dict(
        model=m,
        exclude=[DomainModel.detail_raw],
        extra_attrs=[
            'total_days',
            'expire_days',
        ]
    ), lst))

    return {
        'list': lst,
        'total': total
    }


def get_domain_by_id():
    """
    获取
    :return:
    """
    domain_id = request.json['id']

    row = DomainModel.get_by_id(domain_id)

    return model_to_dict(
        model=row,
        exclude=[DomainModel.detail_raw],
        extra_attrs=[
            'total_days',
            'expire_days',
            'detail',
            'group',
        ]
    )


def update_domain_cert_info_by_id():
    """
    更新域名证书信息
    :return:
    """
    domain_id = request.json['id']

    row = DomainModel.get_by_id(domain_id)

    update_domain_cert_info(row)
