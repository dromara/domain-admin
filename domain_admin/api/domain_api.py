# -*- coding: utf-8 -*-

from flask import request, g, send_file
from playhouse.shortcuts import model_to_dict

from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.service import domain_service
from domain_admin.service import file_service
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

    domain_service.update_domain_cert_info(row)

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

    domain_row = DomainModel.get_by_id(domain_id)

    domain_service.update_domain_cert_info(domain_row)


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
    keyword = request.json.get('keyword')
    group_id = request.json.get('group_id')

    query = DomainModel.select().where(
        DomainModel.user_id == current_user_id
    )

    if isinstance(group_id, int):
        query = query.where(DomainModel.group_id == group_id)

    if keyword:
        query = query.where(DomainModel.domain.contains(keyword))

    lst = query.order_by(
        DomainModel.expire_days.asc(),
        DomainModel.id.desc(),
    ).paginate(page, size)

    total = query.count()

    lst = list(map(lambda m: model_to_dict(
        model=m,
        exclude=[DomainModel.detail_raw],
        extra_attrs=[
            'total_days',
            'expire_days',
            'create_time_label',
            'check_time_label',
            'domain_url',
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
            'domain_url',
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


def import_domain_from_file():
    """
    从文件导入域名
    :return:
    """
    current_user_id = g.user_id

    update_file = request.files.get('file')

    filename = file_service.save_temp_file(update_file)

    count = domain_service.add_domain_from_file(filename, current_user_id)

    return {
        'count': count
    }


def get_all_domain_list_of_user():
    """
    获取用户的所有域名数据
    :return:
    """

    current_user_id = g.user_id
    # temp_filename = domain_service.export_domain_to_file(current_user_id)

    rows = DomainModel.select().where(
        DomainModel.user_id == current_user_id
    )

    lst = [{'domain': row.domain} for row in rows]

    return {
        'list': lst,
        'total': len(lst)
    }
