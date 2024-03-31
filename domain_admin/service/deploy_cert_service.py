# -*- coding: utf-8 -*-
"""
@File    : deploy_cert_service.py
@Date    : 2024-03-31
"""
import traceback

from domain_admin.enums.deploy_status_enum import DeployStatusEnum
from domain_admin.log import logger
from domain_admin.model.certificate_model import CertificateModel
from domain_admin.model.deploy_cert_model import DeployCertModel
from domain_admin.model.host_model import HostModel
from domain_admin.service import issue_certificate_service
from domain_admin.utils import datetime_util


def load_cert_deploy_host(lst):
    """
    @since v1.6.20
    :param lst:
    :return:
    """
    deploy_host_ids = [row['deploy_host_id'] for row in lst]

    deploy_host_rows = HostModel.select().where(
        HostModel.id.in_(deploy_host_ids)
    )

    deploy_host_map = {
        str(row.id): row.to_hidden_dict()
        for row in deploy_host_rows
    }

    for row in lst:
        row['deploy_host'] = deploy_host_map.get(str(row['deploy_host_id']), None)


def handle_deploy_cert(deploy_cert_id):
    """
    根据配置信息部署证书
    @since v1.6.20
    :param deploy_cert_id:
    :return:
    """
    # 部署信息
    deploy_cert_row = DeployCertModel.get_by_id(deploy_cert_id)
    # 部署证书
    cert_row = CertificateModel.get_by_id(deploy_cert_row.cert_id)

    status = DeployStatusEnum.PENDING

    err = None

    # deploy
    try:
        issue_certificate_service.deploy_certificate_file(
            host_id=deploy_cert_row.deploy_host_id,
            key_content=cert_row.ssl_certificate_key,
            pem_content=cert_row.ssl_certificate,
            key_deploy_path=deploy_cert_row.deploy_key_file,
            pem_deploy_path=deploy_cert_row.deploy_fullchain_file,
            reload_cmd=deploy_cert_row.deploy_reloadcmd
        )
        status = DeployStatusEnum.SUCCESS
    except Exception as e:
        err = e
        logger.error(traceback.format_exc())
        status = DeployStatusEnum.ERROR

    # update status
    DeployCertModel.update(
        status=status,
        update_time=datetime_util.get_datetime(),
    ).where(
        DeployCertModel.id == deploy_cert_id
    ).execute()

    return err
