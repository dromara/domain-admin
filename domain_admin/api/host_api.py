# -*- coding: utf-8 -*-
"""
@File    : host_api.py
@Date    : 2023-07-29
"""
from flask import request, g

from domain_admin.config import DEFAULT_SSH_PORT
from domain_admin.enums.role_enum import RoleEnum
from domain_admin.log import logger
from domain_admin.model.host_model import HostModel
from domain_admin.service import auth_service
from domain_admin.utils.flask_ext.app_exception import DataNotFoundAppException


@auth_service.permission(role=RoleEnum.USER)
def add_host():
    """
    添加主机
    :return:
    """
    current_user_id = g.user_id

    host = request.json['host']
    port = request.json.get('port') or DEFAULT_SSH_PORT
    user = request.json['user']
    auth_type = request.json['auth_type']
    private_key = request.json['private_key']
    password = request.json['password']

    row = HostModel.create(
        user_id=current_user_id,
        host=host,
        port=int(port),
        user=user,
        auth_type=auth_type,
        private_key=private_key,
        password=password,
    )

    return row


@auth_service.permission(role=RoleEnum.USER)
def update_host_by_id():
    """
    更新主机
    :return:
    """
    current_user_id = g.user_id

    host_id = request.json['host_id']
    host = request.json['host']
    port = request.json.get('port') or DEFAULT_SSH_PORT
    user = request.json['user']
    password = request.json['password']
    auth_type = request.json['auth_type']
    private_key = request.json['private_key']

    # check data
    host_row = HostModel.select().where(
        HostModel.id == host_id,
        HostModel.user_id == current_user_id
    ).first()

    if not host_row:
        raise DataNotFoundAppException()

    HostModel.update(
        host=host,
        port=int(port),
        user=user,
        password=password,
        auth_type=auth_type,
        private_key=private_key,
    ).where(
        HostModel.id == host_row.id
    ).execute()


@auth_service.permission(role=RoleEnum.USER)
def get_host_by_id():
    """
    获取主机
    :return:
    """
    current_user_id = g.user_id

    host_id = request.json['host_id']

    # check data
    host_row = HostModel.select().where(
        HostModel.id == host_id,
        HostModel.user_id == current_user_id
    ).first()

    if not host_row:
        raise DataNotFoundAppException()

    return host_row


@auth_service.permission(role=RoleEnum.USER)
def delete_host_by_id():
    """
    移除主机
    :return:
    """
    current_user_id = g.user_id

    host_id = request.json['host_id']

    # check data
    host_row = HostModel.select().where(
        HostModel.id == host_id,
        HostModel.user_id == current_user_id
    ).first()

    if not host_row:
        raise DataNotFoundAppException()

    return HostModel.delete_by_id(host_row.id)


@auth_service.permission(role=RoleEnum.USER)
def get_host_list():
    """
    主机列表
    :return:
    """

    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    keyword = request.json.get('keyword')
    host = request.json.get('host')

    query = HostModel.select().where(
        HostModel.user_id == current_user_id
    )

    if keyword:
        query = query.where(HostModel.host.contains(keyword))

    if host:
        query = query.where(HostModel.host == host)

    total = query.count()

    rows = query.order_by(
        HostModel.create_time.desc(),
        HostModel.id.desc()
    ).paginate(page, size)

    return {
        'list': rows,
        'total': total,
    }
