# -*- coding: utf-8 -*-
"""
@File    : certificate_api.py
@Date    : 2024-02-25
"""
from flask import g, request
from peewee import SQL

from domain_admin.model.certificate_model import CertificateModel
from domain_admin.service import certificate_service
from domain_admin.utils.flask_ext.app_exception import AppException, DataNotFoundAppException


def get_certificate_list():
    """
    获取列表
    :return:
    @since v1.6.12
    """

    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)
    keyword = request.json.get('keyword')
    order_prop = request.json.get('order_prop') or 'create_time'
    order_type = request.json.get('order_type') or 'desc'

    if order_type not in ['desc', 'asc']:
        raise AppException('params error: order_type')

    query = CertificateModel.select().where(
        CertificateModel.user_id == current_user_id,
    )

    if keyword:
        query = query.where(CertificateModel.domain.contains(keyword))

    total = query.count()
    lst = []

    if total > 0:
        ordering = [
            SQL(f"`{order_prop}` {order_type}"),
            CertificateModel.id.desc()
        ]

        rows = query.order_by(*ordering).paginate(page, size)

        lst = [row.to_dict() for row in rows]

        # 查询部署数量
        certificate_service.load_cert_deploy_count(lst)

    return {
        "list": lst,
        "total": total
    }


def add_certificate():
    """
    添加
    :return:
    @since v1.6.12
    """

    current_user_id = g.user_id

    domain = request.json['domain']
    ssl_certificate = request.json['ssl_certificate']
    ssl_certificate_key = request.json['ssl_certificate_key']
    start_time = request.json.get('start_time')
    expire_time = request.json.get('expire_time')
    comment = request.json.get('comment') or ''

    data = {
        'user_id': current_user_id,
        'domain': domain,
        'start_time': start_time,
        'expire_time': expire_time,
        'ssl_certificate': ssl_certificate,
        'ssl_certificate_key': ssl_certificate_key,
        'comment': comment,
    }

    CertificateModel.create(**data)


def update_certificate_by_id():
    """
    更新主机地址
    :return:
    @since v1.6.12
    """

    current_user_id = g.user_id

    certificate_id = request.json['certificate_id']

    domain = request.json['domain']
    ssl_certificate = request.json['ssl_certificate']
    ssl_certificate_key = request.json['ssl_certificate_key']
    start_time = request.json.get('start_time')
    expire_time = request.json.get('expire_time')
    comment = request.json.get('comment') or ''

    data = {
        'domain': domain,
        'start_time': start_time,
        'expire_time': expire_time,
        'ssl_certificate': ssl_certificate,
        'ssl_certificate_key': ssl_certificate_key,
        'comment': comment,
    }

    CertificateModel.update(data).where(
        CertificateModel.id == certificate_id
    ).execute()


def delete_certificate_by_id():
    """
    删除
    :return:
    @since v1.6.12
    """

    current_user_id = g.user_id

    certificate_id = request.json['certificate_id']

    CertificateModel.delete().where(
        CertificateModel.id == certificate_id
    ).execute()


def delete_certificate_by_ids():
    """
    批量删除
    :return:
    @since v1.6.12
    """

    current_user_id = g.user_id

    certificate_ids = request.json['certificate_ids']

    CertificateModel.delete().where(
        CertificateModel.id.in_(certificate_ids)
    ).execute()


def get_certificate_by_id():
    """
    获取
    :return:
    @since v1.6.12
    """

    current_user_id = g.user_id

    certificate_id = request.json['certificate_id']
    certificate_row = CertificateModel.get_by_id(certificate_id)

    if not certificate_row:
        raise DataNotFoundAppException()

    # 查询部署数量
    certificate_dict = certificate_row.to_dict()
    certificate_service.load_cert_deploy_count([certificate_dict])

    return certificate_dict
