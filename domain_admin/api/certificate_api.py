# -*- coding: utf-8 -*-
"""
@File    : certificate_api.py
@Date    : 2024-02-25
"""
import json

from flask import g, request
from peewee import SQL

from domain_admin.enums.deploy_status_enum import DeployStatusEnum
from domain_admin.enums.object_enum import ObjectEnum
from domain_admin.enums.role_enum import RoleEnum
from domain_admin.model.certificate_model import CertificateModel
from domain_admin.model.deploy_webhook_model import DeployWebhookModel
from domain_admin.service import certificate_service, auth_service
from domain_admin.utils.flask_ext.app_exception import AppException, DataNotFoundAppException, ForbiddenAppException


@auth_service.permission(role=RoleEnum.USER)
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

    if order_prop not in ['create_time']:
        raise AppException('params error: order_prop')

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

        # 查询api部署状态
        certificate_service.load_api_deploy_status(lst)

    return {
        "list": lst,
        "total": total
    }


@auth_service.permission(role=RoleEnum.USER)
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


@auth_service.permission(role=RoleEnum.USER)
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

    # check data
    certificate_row = CertificateModel.select().where(
        CertificateModel.id == certificate_id,
        CertificateModel.user_id == current_user_id
    ).first()

    if not certificate_row:
        raise DataNotFoundAppException()

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


@auth_service.permission(role=RoleEnum.USER)
def delete_certificate_by_id():
    """
    删除
    :return:
    @since v1.6.12
    """

    current_user_id = g.user_id

    certificate_id = request.json['certificate_id']

    # check data
    certificate_row = CertificateModel.select().where(
        CertificateModel.id == certificate_id,
        CertificateModel.user_id == current_user_id
    ).first()

    if not certificate_row:
        raise DataNotFoundAppException()

    # delete
    CertificateModel.delete().where(
        CertificateModel.id == certificate_row.id
    ).execute()


@auth_service.permission(role=RoleEnum.USER)
def delete_certificate_by_ids():
    """
    批量删除
    :return:
    @since v1.6.12
    """

    current_user_id = g.user_id

    certificate_ids = request.json['certificate_ids']

    CertificateModel.delete().where(
        CertificateModel.id.in_(certificate_ids),
        CertificateModel.user_id == current_user_id
    ).execute()


@auth_service.permission(role=RoleEnum.USER)
def get_certificate_by_id():
    """
    获取
    :return:
    @since v1.6.12
    """

    current_user_id = g.user_id

    certificate_id = request.json['certificate_id']

    # check data
    certificate_row = CertificateModel.select().where(
        CertificateModel.id == certificate_id,
        CertificateModel.user_id == current_user_id
    ).first()

    if not certificate_row:
        raise DataNotFoundAppException()

    # 查询部署数量
    certificate_dict = certificate_row.to_dict()
    certificate_service.load_cert_deploy_count([certificate_dict])

    # 查询api部署状态
    certificate_service.load_api_deploy_status([certificate_dict])

    return certificate_dict


@auth_service.permission(role=RoleEnum.USER)
def deploy_certificate_by_webhook():
    """
    通过webhook部署托管证书
    @since v1.6.52
    """
    current_user_id = g.user_id

    certificate_id = request.json['certificate_id']
    url = request.json['url']
    headers = request.json.get('headers') or {}

    # check data
    certificate_row = certificate_service.get_certificate_row(
        certificate_id=certificate_id,
        user_id=current_user_id
    )

    # update config
    deploy_webhook_row = DeployWebhookModel.select().where(
        DeployWebhookModel.user_id == current_user_id,
        DeployWebhookModel.object_id == certificate_row.id,
        DeployWebhookModel.object_type == ObjectEnum.Certificate
    ).first()

    if not deploy_webhook_row:
        deploy_webhook_row = DeployWebhookModel.create(
            user_id=current_user_id,
            object_id=certificate_row.id,
            object_type=ObjectEnum.Certificate,
            url=url,
            header_raw=json.dumps(headers),
        )
    else:
        DeployWebhookModel.update(
            url=url,
            header_raw=json.dumps(headers),
        ).where(
            DeployWebhookModel.id == deploy_webhook_row.id
        ).execute()

    # refresh
    deploy_webhook_row = DeployWebhookModel.get_by_id(deploy_webhook_row.id)

    # deploy
    res = certificate_service.deploy_certificate_by_webhook(
        certificate_row=certificate_row,
        deploy_webhook_row=deploy_webhook_row,
    )

    # report result
    if res.ok:
        DeployWebhookModel.update(
            status=DeployStatusEnum.SUCCESS
        ).where(
            DeployWebhookModel.id == deploy_webhook_row.id
        ).execute()

        return {
            'result': res.text
        }
    else:
        DeployWebhookModel.update(
            status=DeployStatusEnum.ERROR
        ).where(
            DeployWebhookModel.id == deploy_webhook_row.id
        ).execute()

        raise res.raise_for_status()


@auth_service.permission(role=RoleEnum.USER)
def get_deploy_webhook():
    """
    获取配置部署托管证书
    @since v1.6.52
    """
    current_user_id = g.user_id

    certificate_id = request.json['certificate_id']

    # check data
    certificate_row = certificate_service.get_certificate_row(
        certificate_id=certificate_id,
        user_id=current_user_id
    )

    deploy_webhook_row = DeployWebhookModel.select().where(
        DeployWebhookModel.user_id == current_user_id,
        DeployWebhookModel.object_id == certificate_row.id,
        DeployWebhookModel.object_type == ObjectEnum.Certificate
    ).first()

    if deploy_webhook_row:
        return deploy_webhook_row.to_dict()
