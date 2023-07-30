# -*- coding: utf-8 -*-
"""
@File    : issue_certificate_api.py
@Date    : 2023-07-23
"""
from flask import g, request
from playhouse.shortcuts import model_to_dict

from domain_admin.model.host_model import HostModel
from domain_admin.model.issue_certificate_model import IssueCertificateModel
from domain_admin.service import issue_certificate_service
from domain_admin.utils import ip_util
from domain_admin.utils.acme_util.challenge_type import ChallengeType
from domain_admin.utils.flask_ext.app_exception import AppException


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
        extra_attrs=['domains', 'create_time_label']
    )


def verify_certificate():
    """
    通知验证
    :return:
    """
    current_user_id = g.user_id

    issue_certificate_id = request.json['issue_certificate_id']
    challenge_type = request.json['challenge_type']

    issue_certificate_service.verify_certificate(issue_certificate_id, challenge_type)

    issue_certificate_service.renew_certificate(issue_certificate_id)



def get_certificate_challenges():
    issue_certificate_id = request.json['issue_certificate_id']

    lst = issue_certificate_service.get_certificate_challenges(issue_certificate_id)

    return {
        'total': len(lst),
        'list': lst
    }


def get_domain_host():
    domain = request.json['domain']
    host = ip_util.get_domain_ip(domain)

    return {
        'domain': domain,
        'host': host
    }


def deploy_verify_file():
    """
    部署验证文件
    :return:
    """
    current_user_id = g.user_id

    issue_certificate_id = request.json['issue_certificate_id']
    verify_deploy_path = request.json['verify_deploy_path']
    challenges = request.json['challenges']
    host_id = request.json['host_id']

    if not verify_deploy_path.endswith("/"):
        raise AppException("verify_deploy_path must endswith '/'")

    # deploy
    issue_certificate_service.deploy_verify_file(
        host_id=host_id,
        verify_deploy_path=verify_deploy_path,
        challenges=challenges
    )

    IssueCertificateModel.update(
        deploy_host_id=host_id,
        deploy_verify_path=verify_deploy_path,
    ).where(
        IssueCertificateModel.id == issue_certificate_id
    ).execute()


def deploy_certificate_file():
    current_user_id = g.user_id

    issue_certificate_id = request.json['issue_certificate_id']
    host_id = request.json['host_id']

    key_deploy_path = request.json['key_deploy_path']
    pem_deploy_path = request.json['pem_deploy_path']
    reload_cmd = request.json['reloadcmd']

    host_row = HostModel.get_by_id(host_id)

    host = host_row.host
    user = host_row.user
    password = host_row.password

    issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)

    if not issue_certificate_row.ssl_certificate:
        issue_certificate_service.renew_certificate(issue_certificate_id)
        issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)

    # deploy key
    issue_certificate_service.deploy_certificate_file(
        host_id=host_id,
        issue_certificate_id=issue_certificate_id,
        key_deploy_path=key_deploy_path,
        pem_deploy_path=pem_deploy_path,
        reload_cmd=reload_cmd
    )

    # update only support file verify
    if issue_certificate_row.challenge_type == ChallengeType.HTTP01:
        is_auto_renew = True
    else:
        is_auto_renew = False

    IssueCertificateModel.update(
        deploy_host_id=host_id,
        deploy_key_file=key_deploy_path,
        deploy_fullchain_file=pem_deploy_path,
        deploy_reloadcmd=reload_cmd,
        is_auto_renew=is_auto_renew
    ).where(
        IssueCertificateModel.id == issue_certificate_id
    ).execute()


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
    keyword = request.json.get('keyword')

    query = IssueCertificateModel.select().where(
        IssueCertificateModel.user_id == current_user_id
    )

    if keyword:
        query.where(IssueCertificateModel.domain_raw.contains(keyword))

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

    data = model_to_dict(
        issue_certificate_row,
        extra_attrs=[
            'domains', 'create_time_label', 'domain_validation_urls']
    )

    if data['deploy_host_id']:
        data['deploy_host'] = HostModel.get_by_id(data['deploy_host_id'])
    else:
        data['deploy_host'] = None

    return data


def delete_certificate_by_id():
    """
    获取
    :return:
    """
    current_user_id = g.user_id

    issue_certificate_id = request.json['issue_certificate_id']

    IssueCertificateModel.delete_by_id(issue_certificate_id)


def delete_certificate_by_batch():
    """
    批量删除
    @since v1.2.16
    :return:
    """
    current_user_id = g.user_id

    ids = request.json['ids']

    IssueCertificateModel.delete().where(
        IssueCertificateModel.id.in_(ids),
        IssueCertificateModel.user_id == current_user_id
    ).execute()
