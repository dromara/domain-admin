# -*- coding: utf-8 -*-
"""
@File    : host_api.py
@Date    : 2023-07-29
"""
from flask import request, g

from domain_admin.model.host_model import HostModel


def add_host():
    current_user_id = g.user_id

    host = request.json['host']
    user = request.json['user']
    password = request.json['password']

    row = HostModel.create(
        user_id=current_user_id,
        host=host,
        user=user,
        password=password,
    )

    return row


def update_host_by_id():
    current_user_id = g.user_id

    host_id = request.json['host_id']
    host = request.json['host']
    user = request.json['user']
    password = request.json['password']

    HostModel.update(
        host=host,
        user=user,
        password=password,
    ).where(
        HostModel.id == host_id
    ).execute()

def get_host_by_id():
    host_id = request.json['host_id']

    return HostModel.get_by_id(host_id)

def get_host_list():
    """
    主机列表
    :return:
    """

    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    keyword = request.json.get('keyword')

    query = HostModel.select().where(
        HostModel.user_id == current_user_id
    )

    if keyword:
        query.where(HostModel.host.contains(keyword))

    total = query.count()

    rows = query.order_by(
        HostModel.create_time.desc(),
        HostModel.id.desc()
    ).paginate(page, size)

    return {
        'list': rows,
        'total': total,
    }
