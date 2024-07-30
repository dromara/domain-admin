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

from domain_admin.enums.dns_type_enum import DnsTypeEnum
from domain_admin.enums.host_auth_type_enum import HostAuthTypeEnum
from domain_admin.log import logger
from domain_admin.model.dns_model import DnsModel
from domain_admin.model.host_model import HostModel
from domain_admin.model.issue_certificate_model import IssueCertificateModel, ValidStatus, ChallengeDeployTypeEnum, \
    SSLDeployTypeEnum
from domain_admin.utils import datetime_util, fabric_util, domain_util
from domain_admin.utils.acme_util import acme_v2_api
from domain_admin.utils.acme_util.challenge_type import ChallengeType
from domain_admin.utils.acme_util.directory_type_enum import DirectoryTypeEnum
from domain_admin.utils.acme_util.key_type_enum import KeyTypeEnum
from domain_admin.utils.cert_util import cert_common
from domain_admin.utils.flask_ext.app_exception import AppException
from domain_admin.utils.open_api import aliyun_domain_api, tencentcloud_domain_api, aliyun_oss_api, aliyun_cdn_api, \
    aliyun_dcdn_api
from domain_admin.utils.open_api.aliyun_domain_api import RecordTypeEnum
from domain_admin import config


def issue_certificate(
        domains, user_id,
        directory_type=DirectoryTypeEnum.LETS_ENCRYPT,
        key_type=KeyTypeEnum.RSA
):
    """
    申请新证书
    :param key_type:
    :param directory_type:
    :param domains:
    :param user_id:
    :return:
    """
    # Issue certificate

    # Create domain private key and CSR
    pkey_pem, csr_pem = acme_v2_api.new_csr_comp(domains=domains)

    issue_certificate_row = IssueCertificateModel.create(
        user_id=user_id,
        # challenge_type=challenge_type,
        domain_raw=json.dumps(domains),
        ssl_certificate_key=pkey_pem,
        directory_type=directory_type,
        key_type=key_type,
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

    pkey_pem, csr_pem = acme_v2_api.new_csr_comp(
        domains=domains,
        pkey_pem=pkey_pem,
    )
    print('directory_type', issue_certificate_row.directory_type)

    acme_client = acme_v2_api.get_acme_client(
        directory_type=issue_certificate_row.directory_type,
        key_type=issue_certificate_row.key_type
    )
    orderr = acme_client.new_order(csr_pem)

    # Select HTTP-01 within offered challenges by the CA server
    lst = []

    for domain, domain_challenges in acme_v2_api.select_challenge(orderr).items():
        for challenge in domain_challenges:
            response, validation = challenge.response_and_validation(acme_client.net.key)

            data = {
                'domain': domain,
                'sub_domain': domain_util.get_subdomain(domain),
                'root_domain': domain_util.get_root_domain(domain),
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

    issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)

    items = get_certificate_challenges(issue_certificate_id)
    acme_client = acme_v2_api.get_acme_client(
        directory_type=issue_certificate_row.directory_type,
        key_type=issue_certificate_row.key_type
    )

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

    acme_client = acme_v2_api.get_acme_client(
        directory_type=issue_certificate_row.directory_type,
        key_type=issue_certificate_row.key_type
    )

    # Create domain private key and CSR
    pkey_pem, csr_pem = acme_v2_api.new_csr_comp(
        domains=domains,
        pkey_pem=pkey_pem,
    )

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
    notify_expire_time = now + timedelta(days=config.DEFAULT_RENEW_DAYS)

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
    pkey_pem, csr_pem = acme_v2_api.new_csr_comp(
        domains=row.domains,
    )

    IssueCertificateModel.update(
        ssl_certificate_key=pkey_pem,
        ssl_certificate='',
        start_time=None,
        expire_time=None,
        status=ValidStatus.PENDING,
    ).where(
        IssueCertificateModel.id == row.id
    )

    # 验证文件部署
    if row.challenge_deploy_type_id == ChallengeDeployTypeEnum.SSH:
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

        deploy_verify_file(
            host_id=row.challenge_deploy_id,
            verify_deploy_path=row.deploy_verify_path,
            challenges=challenge_rows
        )
    elif row.challenge_deploy_type_id == ChallengeDeployTypeEnum.DNS:
        # 添加txt记录
        add_dns_domain_record(
            dns_id=row.challenge_deploy_id,
            issue_certificate_id=row.id
        )

    # 验证域名
    verify_certificate(row.id, row.challenge_type)

    # 下载证书
    renew_certificate(row.id)

    # 自动部署，重启服务
    if row.deploy_type_id == SSLDeployTypeEnum.SSH:
        issue_certificate_row = IssueCertificateModel.get_by_id(row.id)

        deploy_certificate_file(
            host_id=row.deploy_host_id,
            key_content=issue_certificate_row.ssl_certificate_key,
            pem_content=issue_certificate_row.ssl_certificate,
            key_deploy_path=row.deploy_key_file,
            pem_deploy_path=row.deploy_fullchain_file,
            reload_cmd=row.deploy_reloadcmd
        )
    elif row.deploy_type_id == SSLDeployTypeEnum.WEB_HOOK:
        deploy_ssl_by_web_hook(
            issue_certificate_id=row.id,
            url=row.deploy_url,
            headers=row.deploy_header,
        )

    elif row.deploy_type_id == SSLDeployTypeEnum.OSS:
        deploy_cert_to_oss(
            issue_certificate_id=row.id,
            dns_id=row.deploy_host_id
        )

    elif row.deploy_type_id == SSLDeployTypeEnum.CDN:
        deploy_cert_to_cdn(
            issue_certificate_id=row.id,
            dns_id=row.deploy_host_id
        )
    elif row.deploy_type_id == SSLDeployTypeEnum.DCDN:
        deploy_cert_to_dcdn(
            issue_certificate_id=row.id,
            dns_id=row.deploy_host_id
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


def add_dns_domain_record(dns_id, issue_certificate_id):
    """
    添加dns记录
    :param dns_id:
    :param issue_certificate_id:
    :return:
    """
    dns_row = DnsModel.get_by_id(dns_id)

    # 获取验证方式
    challenge_list = get_certificate_challenges(issue_certificate_id)

    for challenge_row in challenge_list:
        challenge_json = challenge_row['challenge'].to_json()
        if challenge_json['type'] == ChallengeType.DNS01:

            if challenge_row['sub_domain']:
                record_key = '_acme-challenge.' + challenge_row['sub_domain']
            else:
                record_key = '_acme-challenge'
            if dns_row.dns_type_id == DnsTypeEnum.ALIYUN:
                aliyun_domain_api.add_domain_record(
                    access_key_id=dns_row.access_key,
                    access_key_secret=dns_row.secret_key,
                    domain_name=challenge_row['root_domain'],
                    record_type=RecordTypeEnum.TXT,
                    record_key=record_key,
                    record_value=challenge_row['validation']
                )
            elif dns_row.dns_type_id == DnsTypeEnum.TENCENT_CLOUD:
                tencentcloud_domain_api.add_domain_record(
                    access_key_id=dns_row.access_key,
                    access_key_secret=dns_row.secret_key,
                    domain_name=challenge_row['root_domain'],
                    record_type=RecordTypeEnum.TXT,
                    record_key=record_key,
                    record_value=challenge_row['validation']
                )


def deploy_ssl_by_web_hook(issue_certificate_id, url, headers):
    """
    通过webhook部署ssl证书
    :param issue_certificate_id:
    :param url:
    :param headers:
    :return:
    """
    issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)

    if not issue_certificate_row:
        raise AppException('数据不存在')

    data = {
        'domains': issue_certificate_row.domains,
        'ssl_certificate': issue_certificate_row.ssl_certificate,
        'ssl_certificate_key': issue_certificate_row.ssl_certificate_key,
        'start_time': datetime_util.format_datetime(issue_certificate_row.start_time),
        'expire_time': datetime_util.format_datetime(issue_certificate_row.expire_time),
    }

    res = requests.request(
        method='POST',
        url=url,
        headers=headers,
        json=data
    )

    if not res.ok:
        raise res.raise_for_status()

    return res.text


def deploy_cert_to_oss(issue_certificate_id, dns_id):
    """
    部署ssl证书到oss
    """
    issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)

    if not issue_certificate_row:
        raise AppException('证书数据不存在')

    dns_row = DnsModel.get_by_id(dns_id)
    if not dns_row:
        raise AppException('DNS数据不存在')

    domain = issue_certificate_row.domains[0]

    oss_info = aliyun_oss_api.cname_to_oss_info(domain)
    if not oss_info:
        raise AppException('dns 未设置')

    logger.info("oss_info: %s", oss_info)

    aliyun_oss_api.put_bucket_cname(
        access_key_id=dns_row.access_key,
        access_key_secret=dns_row.secret_key,
        bucket_name=oss_info['bucket_name'],
        domain=domain,
        certificate=issue_certificate_row.ssl_certificate,
        private_key=issue_certificate_row.ssl_certificate_key,
        endpoint=oss_info['endpoint'],
    )


def deploy_cert_to_cdn(issue_certificate_id, dns_id):
    """
    部署ssl证书到cdn
    """
    issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)

    if not issue_certificate_row:
        raise AppException('证书数据不存在')

    dns_row = DnsModel.get_by_id(dns_id)
    if not dns_row:
        raise AppException('DNS数据不存在')

    domain = issue_certificate_row.domains[0]

    # oss_info = aliyun_oss_api.cname_to_oss_info(domain)
    # if not oss_info:
    #     raise AppException('dns 未设置')
    #
    # logger.info("oss_info: %s", oss_info)

    aliyun_cdn_api.set_cdn_domain_ssl_certificate_v2(
        access_key_id=dns_row.access_key,
        access_key_secret=dns_row.secret_key,
        domain_name=domain,
        certificate=issue_certificate_row.ssl_certificate,
        private_key=issue_certificate_row.ssl_certificate_key,
    )


def deploy_cert_to_dcdn(issue_certificate_id, dns_id):
    """
    部署ssl证书到dcdn
    """
    issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)

    if not issue_certificate_row:
        raise AppException('证书数据不存在')

    dns_row = DnsModel.get_by_id(dns_id)
    if not dns_row:
        raise AppException('DNS数据不存在')

    domain = issue_certificate_row.domains[0]

    aliyun_dcdn_api.set_dcdn_domain_ssl_certificate(
        access_key_id=dns_row.access_key,
        access_key_secret=dns_row.secret_key,
        domain_name=domain,
        certificate=issue_certificate_row.ssl_certificate,
        private_key=issue_certificate_row.ssl_certificate_key,
    )


def check_auto_renew(issue_certificate_id):
    """
    首次申请，自动判断是否可以自动续期
    :param issue_certificate_id:
    :return:
    """
    issue_certificate_row = IssueCertificateModel.get_by_id(issue_certificate_id)

    if issue_certificate_row.can_auto_renew:
        IssueCertificateModel.update(
            is_auto_renew=True
        ).where(
            IssueCertificateModel.id == issue_certificate_id
        ).execute()
