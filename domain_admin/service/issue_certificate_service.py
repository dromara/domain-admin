# -*- coding: utf-8 -*-
"""
@File    : issue_certificate_service.py
@Date    : 2023-07-23
"""
import json
import time
import traceback
from datetime import datetime, timedelta

import OpenSSL
import requests

from domain_admin.enums.host_auth_type_enum import HostAuthTypeEnum
from domain_admin.log import logger
from domain_admin.model.host_model import HostModel
from domain_admin.model.issue_certificate_model import IssueCertificateModel
from domain_admin.utils import datetime_util, fabric_util, domain_util
from domain_admin.utils.acme_util import acme_v2_api
from domain_admin.utils.acme_util.challenge_type import ChallengeType
from domain_admin.utils.cert_util import cert_common
from domain_admin.utils.flask_ext.app_exception import AppException


def issue_certificate(domains, user_id):
    """
    申请新证书
    :param domains:
    :param user_id:
    :return:
    """
    # Issue certificate

    # Create domain private key and CSR
    pkey_pem, csr_pem = acme_v2_api.new_csr_comp(domains)

    issue_certificate_row = IssueCertificateModel.create(
        user_id=user_id,
        # challenge_type=challenge_type,
        domain_raw=json.dumps(domains),
        ssl_certificate_key=pkey_pem,
        # status='pending',
    )

    return issue_certificate_row


def get_certificate_challenges(issue_certificate_id):
    """
    获取验证方式
    :param issue_certificate_id:
    :return:
    """
    issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)
    # Create domain private key and CSR
    domains = issue_certificate_row.domains
    pkey_pem = issue_certificate_row.ssl_certificate_key

    pkey_pem, csr_pem = acme_v2_api.new_csr_comp(domains, pkey_pem)

    acme_client = acme_v2_api.get_acme_client()
    orderr = acme_client.new_order(csr_pem)

    # Select HTTP-01 within offered challenges by the CA server
    lst = []

    for domain, domain_challenges in acme_v2_api.select_challenge(orderr).items():
        for challenge in domain_challenges:
            response, validation = challenge.response_and_validation(acme_client.net.key)

            data = {
                'domain': domain,
                'sub_domain': domain_util.get_subdomain(domain),
                'validation': validation,
                'challenge': challenge
            }

            lst.append(data)

    return lst


def verify_certificate(issue_certificate_id, challenge_type):
    """
    验证域名
    :param issue_certificate_id:
    :param challenge_type:
    :return:
    """
    items = get_certificate_challenges(issue_certificate_id)
    acme_client = acme_v2_api.get_acme_client()

    verify_count = 0
    for item in items:
        challenge = item['challenge']
        challenge_json = challenge.to_json()

        # 指定认证类型
        if challenge_type != challenge_json['type']:
            continue

        response, validation = challenge.response_and_validation(acme_client.net.key)
        logger.info(validation)

        # Let the CA server know that we are ready for the challenge.
        acme_client.answer_challenge(challenge, response)

        count = 0
        max_count = 5

        while True:
            count += 1

            status = get_challenge_status(challenge_json['url'])

            if status == 'valid':
                IssueCertificateModel.update(
                    status=status,
                    update_time=datetime_util.get_datetime()
                ).where(
                    IssueCertificateModel.id == issue_certificate_id
                ).execute()

                break

            if count >= max_count:
                raise AppException("域名验证失败：{}".format(item['domain']))

            time.sleep(count)
        verify_count += 1

    if verify_count == 0:
        raise AppException("域名验证失败")

    # if success update challenge_type
    IssueCertificateModel.update(
        challenge_type=challenge_type,
    ).where(
        IssueCertificateModel.id == issue_certificate_id
    ).execute()


def renew_certificate(row_id):
    """
    Renew certificate
    :param row_id:
    :return:
    """
    issue_certificate_row = IssueCertificateModel.get_by_id(row_id)

    pkey_pem = issue_certificate_row.ssl_certificate_key
    domains = issue_certificate_row.domains

    acme_client = acme_v2_api.get_acme_client()

    # Create domain private key and CSR
    pkey_pem, csr_pem = acme_v2_api.new_csr_comp(domains, pkey_pem)

    orderr = acme_client.new_order(csr_pem)

    # Select HTTP-01 within offered challenges by the CA server
    # challb = acme_v2_api.select_challenge(orderr, challenge_type)
    # logger.debug(json_util.json_dump(challb.to_json()))

    # Performing challenge

    fullchain_pem = acme_v2_api.perform_http01(acme_client, orderr)

    logger.debug(fullchain_pem)

    fullchain_com = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM, fullchain_pem
    )

    cert = cert_common.parse_cert(fullchain_com)

    IssueCertificateModel.update(
        ssl_certificate=fullchain_pem,
        start_time=cert.notBefore,
        expire_time=cert.notAfter,
        update_time=datetime_util.get_datetime()
    ).where(
        IssueCertificateModel.id == issue_certificate_row.id
    ).execute()


def get_challenge_status(url):
    """
    :param url:
    :return:
    {
        "type": "http-01",
        "status": "valid",
        "url": "https://acme-staging-v02.api.letsencrypt.org/acme/chall-v3/8189968164/2x43yw",
        "token": "uEy2gzPlQN1IIE541sbRK23AQWFh87MvmvzMDOUvIKk",
        "validationRecord": [],
        "validated": "2023-07-23T08:59:59Z"
    }
    """
    logger.debug(url)

    res = requests.get(url)

    data = res.json()
    logger.debug(data)

    return data['status']


def renew_all_certificate():
    """
    更新所有证书
    :return:
    """

    now = datetime.now()
    notify_expire_time = now + timedelta(days=30)

    rows = IssueCertificateModel.select().where(
        (IssueCertificateModel.is_auto_renew == True)
        & (
                (IssueCertificateModel.expire_time <= notify_expire_time)
                | (IssueCertificateModel.expire_time == None)
        )
    ).order_by(IssueCertificateModel.expire_time.asc())

    for row in rows:
        try:
            renew_certificate_row(row)
        except Exception as e:
            logger.error(traceback.format_exc())


def renew_certificate_row(row):
    """
    证书自动续期
    :param row:
    :return:
    """
    # 重新申请
    pkey_pem, csr_pem = acme_v2_api.new_csr_comp(row.domains)

    IssueCertificateModel.update(
        ssl_certificate_key=pkey_pem,
        ssl_certificate='',
        start_time=None,
        expire_time=None,
        status='pending',
    ).where(
        IssueCertificateModel.id == row.id
    )

    # 获取验证方式
    challenge_list = get_certificate_challenges(row.id)

    challenge_rows = []
    for challenge_row in challenge_list:
        challenge_json = challenge_row['challenge'].to_json()
        if challenge_json['type'] == ChallengeType.HTTP01:
            challenge_rows.append({
                'token': challenge_json['token'],
                'validation': challenge_row['validation']
            })

    # 验证文件部署
    deploy_verify_file(
        host_id=row.deploy_host_id,
        verify_deploy_path=row.deploy_verify_path,
        challenges=challenge_rows
    )

    # 验证域名
    verify_certificate(row.id, ChallengeType.HTTP01)

    # 下载证书
    renew_certificate(row.id)

    # 自动部署，重启服务
    issue_certificate_row = IssueCertificateModel.get_by_id(row.id)

    deploy_certificate_file(
        host_id=row.deploy_host_id,
        key_content=issue_certificate_row.ssl_certificate_key,
        pem_content=issue_certificate_row.ssl_certificate,
        key_deploy_path=row.deploy_key_file,
        pem_deploy_path=row.deploy_fullchain_file,
        reload_cmd=row.deploy_reloadcmd
    )


def deploy_verify_file(host_id, verify_deploy_path, challenges):
    """
    部署验证文件
    :return:
    """
    logger.info(challenges)

    host_row = HostModel.get_by_id(host_id)

    host = host_row.host
    port = host_row.port
    user = host_row.user
    password = host_row.password
    private_key = host_row.private_key
    auth_type = host_row.auth_type

    for row in challenges:
        if not row['token']:
            raise AppException('token is empty')

        verify_deploy_filename = verify_deploy_path + row['token']

        if not verify_deploy_filename:
            raise AppException('verify_deploy_filename is empty')

        logger.debug("verify_deploy_filename: %s", verify_deploy_filename)

        if not row['validation']:
            raise AppException('validation is empty')

        if auth_type == HostAuthTypeEnum.PRIVATE_KEY:
            fabric_util.deploy_file_by_key(
                host=host,
                port=port,
                user=user,
                private_key=private_key,
                content=row['validation'],
                remote=verify_deploy_filename
            )
        else:
            fabric_util.deploy_file(
                host=host,
                port=port,
                user=user,
                password=password,
                content=row['validation'],
                remote=verify_deploy_filename
            )


def deploy_certificate_file(
        host_id,
        key_content,
        key_deploy_path,
        pem_content,
        pem_deploy_path,
        reload_cmd
):
    """
    自动部署SSL证书到服务器
    :param host_id: 主机id

    :param key_deploy_path: 私钥部署路径
    :param key_content: 私钥内容

    :param pem_deploy_path: 公钥部署路径
    :param pem_content: 公钥内容

    :param reload_cmd: 重启命令
    :return:
    """
    host_row = HostModel.get_by_id(host_id)

    host = host_row.host
    port = host_row.port
    user = host_row.user
    password = host_row.password
    auth_type = host_row.auth_type
    private_key = host_row.private_key

    # deploy key
    if key_deploy_path:
        if auth_type == HostAuthTypeEnum.PRIVATE_KEY:
            fabric_util.deploy_file_by_key(
                host=host,
                port=port,
                user=user,
                private_key=private_key,
                content=key_content,
                remote=key_deploy_path
            )
        else:
            fabric_util.deploy_file(
                host=host,
                port=port,
                user=user,
                password=password,
                content=key_content,
                remote=key_deploy_path
            )

    # deploy ssl_certificate
    if pem_deploy_path:
        if auth_type == HostAuthTypeEnum.PRIVATE_KEY:
            fabric_util.deploy_file_by_key(
                host=host,
                port=port,
                user=user,
                private_key=private_key,
                content=pem_content,
                remote=pem_deploy_path
            )
        else:
            fabric_util.deploy_file(
                host=host,
                port=port,
                user=user,
                password=password,
                content=pem_content,
                remote=pem_deploy_path
            )

    # reload
    if reload_cmd:
        if auth_type == HostAuthTypeEnum.PRIVATE_KEY:
            fabric_util.run_command_by_key(
                host=host,
                port=port,
                user=user,
                private_key=private_key,
                command=reload_cmd
            )
        else:
            fabric_util.run_command(
                host=host,
                port=port,
                user=user,
                password=password,
                command=reload_cmd
            )
