# -*- coding: utf-8 -*-

from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.model import DomainModel, GroupModel
from domain_admin.service import domain_service
from domain_admin.utils import datetime_util
from domain_admin.utils.flask_ext.app_exception import AppException
from domain_admin.utils.peewee_ext import model_util


def add_domain():
    """
    添加域名
    :return:
    """

    current_user_id = g.user_id

    domain = request.json.get('domain')
    alias = request.json.get('alias', '')
    group_id = request.json.get('group_id', 0)

    if not domain:
        raise AppException('参数缺失：domain')

    row = domain_service.add_domain({
        'user_id': current_user_id,
        'domain': domain,
        'alias': alias,
        'group_id': group_id,
    })

    return {'id': row.id}


def update_domain_by_id():
    """
    更新数据
    id domain alias group_id notify_status
    :return:
    """
    current_user_id = g.user_id

    data = request.json
    domain_id = data.pop('id')

    domain_service.check_permission_and_get_row(domain_id, current_user_id)

    data['update_time'] = datetime_util.get_datetime()

    DomainModel.update(data).where(
        DomainModel.id == domain_id
    ).execute()


def delete_domain_by_id():
    """
    删除
    :return:
    """
    current_user_id = g.user_id

    domain_id = request.json['id']

    domain_service.check_permission_and_get_row(domain_id, current_user_id)

    DomainModel.delete_by_id(domain_id)


def get_domain_list():
    """
    获取域名列表
    :return:
    """
    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    group_id = request.json.get('group_id')

    query = DomainModel.select().where(
        DomainModel.user_id == current_user_id
    )

    if isinstance(group_id, int):
        query = query.where(DomainModel.group_id == group_id)

    lst = query.order_by(
        DomainModel.create_time.asc(),
        DomainModel.id.asc(),
    ).paginate(page, size)

    total = query.count()

    lst = list(map(lambda m: model_to_dict(
        model=m,
        exclude=[DomainModel.detail_raw],
        extra_attrs=[
            'total_days',
            'expire_days',
        ]
    ), lst))

    lst = model_util.list_with_relation_one(lst, 'group', GroupModel)

    return {
        'list': lst,
        'total': total
    }


def get_domain_by_id():
    """
    获取
    :return:
    """
    current_user_id = g.user_id

    domain_id = request.json['id']

    row = domain_service.check_permission_and_get_row(domain_id, current_user_id)

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


def update_all_domain_cert_info():
    """
    更新所有域名证书信息
    :return:
    """

    domain_service.update_all_domain_cert_info()


def update_all_domain_cert_info_of_user():
    """
    更新当前用户的所有域名信息
    :return:
    """
    current_user_id = g.user_id
    domain_service.update_all_domain_cert_info_of_user(current_user_id)


def update_domain_cert_info_by_id():
    """
    更新域名证书信息
    :return:
    """
    current_user_id = g.user_id

    domain_id = request.json['id']

    row = domain_service.check_permission_and_get_row(domain_id, current_user_id)

    domain_service.update_domain_cert_info(row)


def send_domain_info_list_email():
    """
    发送域名证书信息到邮箱
    :return:
    """
    current_user_id = g.user_id

    domain_service.send_domain_list_email(current_user_id)


def check_domain_cert():
    """
    检查域名证书信息
    :return:
    """
    current_user_id = g.user_id

    # 先更新，再检查
    domain_service.update_all_domain_cert_info_of_user(current_user_id)

    domain_service.check_domain_cert(current_user_id)
