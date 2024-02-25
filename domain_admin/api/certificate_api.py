# -*- coding: utf-8 -*-
"""
@File    : certificate_api.py
@Date    : 2024-02-25
"""
from flask import g, request

from domain_admin.model.certificate_model import CertificateModel


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

    query = CertificateModel.select().where(
        CertificateModel.user_id == current_user_id,
    )

    if keyword:
        query = query.where(CertificateModel.domain.contains(keyword))

    total = query.count()
    lst = []

    if total > 0:
        rows = query.order_by(
            CertificateModel.id.desc()
        ).paginate(page, size)

        lst = [row.to_dict() for row in rows]

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

    if certificate_row:
        return certificate_row.to_dict()

