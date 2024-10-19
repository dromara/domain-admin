# -*- coding: utf-8 -*-
"""
@File    : certificate_service.py
@Date    : 2024-03-31
"""
import requests
from peewee import fn

from domain_admin.enums.deploy_status_enum import DeployStatusEnum
from domain_admin.enums.object_enum import ObjectEnum
from domain_admin.model.certificate_model import CertificateModel
from domain_admin.model.deploy_cert_model import DeployCertModel
from domain_admin.model.deploy_webhook_model import DeployWebhookModel
from domain_admin.utils import datetime_util
from domain_admin.utils.flask_ext.app_exception import DataNotFoundAppException


def load_cert_deploy_count(lst):
    cert_ids = [row['id'] for row in lst]

    cert_deploy_rows = DeployCertModel.select().where(
        DeployCertModel.cert_id.in_(cert_ids)
    )

    for row in lst:
        row['deploy_count'] = len([
            cert_deploy_row
            for cert_deploy_row in cert_deploy_rows
            if cert_deploy_row.cert_id == row['id']
        ])

        row['deploy_pending_count'] = len([
            cert_deploy_row
            for cert_deploy_row in cert_deploy_rows
            if cert_deploy_row.cert_id == row['id'] and cert_deploy_row.status == DeployStatusEnum.PENDING
        ])

        row['deploy_error_count'] = len([
            cert_deploy_row
            for cert_deploy_row in cert_deploy_rows
            if cert_deploy_row.cert_id == row['id'] and cert_deploy_row.status == DeployStatusEnum.ERROR
        ])

        row['deploy_success_count'] = row['deploy_count'] - row['deploy_error_count'] - row['deploy_pending_count']


def get_certificate_row(certificate_id, user_id):
    # check data
    certificate_row = CertificateModel.select().where(
        CertificateModel.id == certificate_id,
        CertificateModel.user_id == user_id
    ).first()

    if not certificate_row:
        raise DataNotFoundAppException()

    return certificate_row


def deploy_certificate_by_webhook(
        certificate_row: CertificateModel,
        deploy_webhook_row: DeployWebhookModel
):
    """
    @since v1.6.52
    """

    data = {
        'domain': certificate_row.domain,
        'ssl_certificate': certificate_row.ssl_certificate,
        'ssl_certificate_key': certificate_row.ssl_certificate_key,
        'start_time': datetime_util.format_datetime(certificate_row.start_time),
        'expire_time': datetime_util.format_datetime(certificate_row.expire_time),
    }

    res = requests.request(
        method='POST',
        url=deploy_webhook_row.url,
        headers=deploy_webhook_row.headers,
        json=data
    )

    return res


def load_api_deploy_status(lst):
    cert_ids = [row['id'] for row in lst]

    deploy_webhook_rows = DeployWebhookModel.select().where(
        DeployWebhookModel.object_id.in_(cert_ids)
    )
    deploy_webhook_map = {row.object_id: row for row in deploy_webhook_rows}
    for row in lst:
        deploy_webhook_row = deploy_webhook_map.get(row['id'])
        row['api_deploy_status'] = deploy_webhook_row.status if deploy_webhook_row else None

    return None
