# -*- coding: utf-8 -*-

"""
address_api.py
"""
from flask import request, g
from peewee import fn
from playhouse.shortcuts import model_to_dict

from domain_admin.model.address_model import AddressModel
from domain_admin.model.domain_model import DomainModel
from domain_admin.model.group_model import GroupModel
from domain_admin.service import async_task_service
from domain_admin.service import domain_service, global_data_service
from domain_admin.service import file_service
from domain_admin.utils import datetime_util
from domain_admin.utils.flask_ext.app_exception import AppException


def get_address_list_by_domain_id():
    """
    通过域名id获取关联的主机地址列表
    :return:
    @since v1.3.1
    """

    current_user_id = g.user_id

    domain_id = request.json['domain_id']
    page = request.json.get('page', 1)
    size = request.json.get('size', 10)

    query = AddressModel.select().where(
        AddressModel.domain_id == domain_id
    )

    total = query.count()
    if total > 0:
        rows = query.paginate(page, size)
        lst = list(map(lambda m: model_to_dict(
            model=m,
            extra_attrs=[
                'ssl_start_date',
                'ssl_expire_date',
                'real_time_ssl_expire_days',
                'ssl_check_time_label',
            ]
        ), rows))
    else:
        lst = []

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
    ssl_auto_update = request.json.get('ssl_auto_update', True)
    ssl_expire_monitor = request.json.get('ssl_expire_monitor', True)

    address_row = AddressModel.create(
        domain_id=domain_id,
        host=host,
        ssl_start_time=ssl_start_time,
        ssl_expire_time=ssl_expire_time,
        ssl_auto_update=ssl_auto_update,
        ssl_expire_monitor=ssl_expire_monitor,
    )

    domain_service.update_address_row_info_with_sync_domain_row(address_row.address_id)


def delete_address_by_id():
    """
    删除主机地址
    :return:
    @since v1.3.1
    """

    current_user_id = g.user_id

    address_id = request.json['address_id']

    AddressModel.delete().where(
        AddressModel.id == address_id
    ).execute()


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
    ssl_auto_update = request.json.get('ssl_auto_update', True)
    ssl_expire_monitor = request.json.get('ssl_expire_monitor', True)

    AddressModel.update(
        host=host,
        ssl_start_time=ssl_start_time,
        ssl_expire_time=ssl_expire_time,
        ssl_auto_update=ssl_auto_update,
        ssl_expire_monitor=ssl_expire_monitor,
    ).where(
        AddressModel.id == address_id
    ).execute()

    domain_service.update_address_row_info_with_sync_domain_row(address_id)


def update_address_list_info_by_domain_id():
    """
    更新主机地址信息
    :return:
    @since v1.3.1
    """

    current_user_id = g.user_id

    domain_id = request.json['domain_id']
    domain_row = DomainModel.get_by_id(domain_id)
    err = domain_service.update_domain_address_info(domain_row)

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
