# -*- coding: utf-8 -*-
"""
@File    : issue_certificate_api.py
@Date    : 2023-07-23
"""
from flask import g, request
from playhouse.shortcuts import model_to_dict

from domain_admin.model.issue_certificate_model import IssueCertificateModel
from domain_admin.service import issue_certificate_service


def issue_certificate():
    """
    发起申请
    :return:
    """
    current_user_id = g.user_id

    domains = request.json['domains']

    issue_certificate_id = issue_certificate_service.issue_certificate(domains, current_user_id)

    issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)

    return model_to_dict(
        issue_certificate_row,
        extra_attrs=['domains', 'create_time_label', 'domain_validation_urls']
    )


def verify_certificate():
    """
    通知验证
    :return:
    """
    current_user_id = g.user_id

    issue_certificate_id = request.json['issue_certificate_id']

    issue_certificate_service.verify_certificate(issue_certificate_id)


def renew_certificate():
    """
    发起申请
    :return:
    """
    current_user_id = g.user_id

    issue_certificate_id = request.json['issue_certificate_id']

    issue_certificate_service.renew_certificate(issue_certificate_id)

    issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)

    return model_to_dict(
        issue_certificate_row,
        extra_attrs=['domains', 'create_time_label', 'domain_validation_urls']
    )


def get_certificate_list():
    """
    发起申请
    :return:
    """
    current_user_id = g.user_id
    page = request.json.get('page', 1)
    size = request.json.get('size', 10)

    query = IssueCertificateModel.select().where(
        IssueCertificateModel.user_id == current_user_id
    )

    total = query.count()

    rows = query.order_by(
        IssueCertificateModel.create_time.desc(),
        IssueCertificateModel.id.desc()
    ).paginate(page, size)

    lst = [model_to_dict(
        row,
        extra_attrs=['domains', 'create_time_label', 'domain_validation_urls'],
        exclude=[
            IssueCertificateModel.ssl_certificate,
            IssueCertificateModel.ssl_certificate_key
        ])
        for row in rows]

    return {
        'list': lst,
        'total': total,
    }


def get_issue_certificate_by_id():
    """
    获取
    :return:
    """
    current_user_id = g.user_id

    issue_certificate_id = request.json['issue_certificate_id']

    issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)

    return model_to_dict(
        issue_certificate_row,
        extra_attrs=[
            'domains', 'create_time_label', 'domain_validation_urls']
    )
