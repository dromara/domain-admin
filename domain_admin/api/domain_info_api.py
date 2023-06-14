# -*- coding: utf-8 -*-
"""
domain_info_api.py
"""
from flask import request, g
from peewee import fn
from playhouse.shortcuts import model_to_dict

from domain_admin.model.domain_info_model import DomainInfoModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.service import group_service, domain_info_service
from domain_admin.utils import domain_util
from domain_admin.utils.flask_ext.app_exception import AppException


def add_domain_info():
    """
    添加域名
    :return:
    """

    current_user_id = g.user_id

    domain = domain_util.get_root_domain(request.json['domain'])
    domain_start_time = request.json.get('domain_start_time')
    domain_expire_time = request.json.get('domain_expire_time')
    is_auto_update = request.json.get('is_auto_update', True)
    is_expire_monitor = request.json.get('is_expire_monitor', True)

    row = DomainInfoModel.create(
        domain=domain,
        user_id=current_user_id,
        domain_start_time=domain_start_time,
        domain_expire_time=domain_expire_time,
        is_auto_update=is_auto_update,
        is_expire_monitor=is_expire_monitor,
    )

    if is_auto_update:
        domain_info_service.update_domain_info_row(row)

    return {'domain_info_id': row.id}


def update_domain_info_by_id():
    """
    更新数据
    :return:
    """

    current_user_id = g.user_id

    domain_info_id = request.json['domain_info_id']
    domain = domain_util.get_root_domain(request.json['domain'])
    domain_start_time = request.json.get('domain_start_time')
    domain_expire_time = request.json.get('domain_expire_time')
    is_auto_update = request.json.get('is_auto_update', True)
    is_expire_monitor = request.json.get('is_expire_monitor', True)

    data = {
        'domain': domain,
        'is_auto_update': is_auto_update,
        'is_expire_monitor': is_expire_monitor
    }

    # 不自动更新，才可以提交开始时间和结束时间
    if is_auto_update is False:
        data['domain_start_time'] = domain_start_time
        data['domain_expire_time'] = domain_expire_time

    DomainInfoModel.update(data).where(
        DomainInfoModel.id == domain_info_id
    ).execute()


def update_domain_info_field_by_id():
    """
    更新单个数据
    :return:
    """

    current_user_id = g.user_id

    domain_info_id = request.json['domain_info_id']
    field = request.json.get('field')
    value = request.json.get('value')

    if field not in ['is_auto_update', 'is_expire_monitor']:
        raise AppException("not allow field")

    data = {
        field: value,
    }

    DomainInfoModel.update(data).where(
        DomainInfoModel.id == domain_info_id
    ).execute()


def delete_domain_info_by_id():
    """
    删除
    :return:
    """
    current_user_id = g.user_id

    domain_info_id = request.json['domain_info_id']

    DomainInfoModel.delete_by_id(domain_info_id)


def get_domain_info_by_id():
    """
    获取
    :return:
    """
    current_user_id = g.user_id

    domain_info_id = request.json['domain_info_id']

    return DomainInfoModel.get_by_id(domain_info_id)


def get_domain_info_list():
    """
    获取域名列表
    :return:
    """
    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    keyword = request.json.get('keyword')

    # 列表数据
    query = DomainInfoModel.select().where(
        DomainInfoModel.user_id == current_user_id
    )

    if keyword:
        query = query.where(DomainInfoModel.domain.contains(keyword))

    total = query.count()

    lst = []
    if total > 0:

        rows = query.order_by(
            DomainInfoModel.domain_expire_days.asc(),
            DomainInfoModel.id.desc()
        ).paginate(page, size)

        lst = [model_to_dict(
            model=row,
            extra_attrs=[
                'real_domain_expire_days',
                'update_time_label',
            ]
        ) for row in rows]

        domain_list = [row['domain'] for row in lst]

        # 域名证书
        root_domain_groups = DomainModel.select(
            DomainModel.root_domain,
            fn.COUNT(DomainModel.id).alias('count')
        ).where(
            DomainModel.root_domain.in_(domain_list)
        ).group_by(DomainModel.root_domain)

        root_domain_groups_map = {
            row.root_domain: row.count
            for row in root_domain_groups
        }

        for row in lst:
            row['ssl_count'] = root_domain_groups_map.get(row['domain'], 0)

    return {
        'list': lst,
        'total': total,
    }


def update_domain_info_row_by_id():
    domain_info_id = request.json['domain_info_id']

    row = DomainInfoModel.get_by_id(domain_info_id)

    domain_info_service.update_domain_info_row(row)
