# -*- coding: utf-8 -*-
"""
@File    : certificate_service.py
@Date    : 2024-03-31
"""
from peewee import fn

from domain_admin.enums.deploy_status_enum import DeployStatusEnum
from domain_admin.model.deploy_cert_model import DeployCertModel


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
