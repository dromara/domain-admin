# -*- coding: utf-8 -*-
"""
@File    : issue_certificate_service.py
@Date    : 2023-07-23
"""
import json
import time

import OpenSSL
import requests

from domain_admin.log import logger
from domain_admin.model.issue_certificate_model import IssueCertificateModel
from domain_admin.utils import datetime_util
from domain_admin.utils.acme_util import acme_v2_api
from domain_admin.utils.cert_util import cert_common
from domain_admin.utils.flask_ext.app_exception import AppException


def issue_certificate(domains, user_id):
    # Issue certificate
    acme_client = acme_v2_api.get_acme_client()

    # Create domain private key and CSR
    pkey_pem, csr_pem = acme_v2_api.new_csr_comp(domains)

    issue_certificate_row = IssueCertificateModel.create(
        user_id=user_id,
        domain_raw=json.dumps(domains),
        ssl_certificate_key=pkey_pem,
        status='pending',
    )

    orderr = acme_client.new_order(csr_pem)

    # Select HTTP-01 within offered challenges by the CA server
    challb = acme_v2_api.select_http01_chall(orderr)
    logger.debug(challb.to_json())

    response, validation = challb.response_and_validation(acme_client.net.key)

    IssueCertificateModel.update(
        status_url=challb.to_json()['url'],
        token=challb.to_json()['token'],
        validation=validation,
        update_time=datetime_util.get_datetime()
    ).where(
        IssueCertificateModel.id == issue_certificate_row.id
    ).execute()

    return issue_certificate_row.id


def verify_certificate(row_id):
    issue_certificate_row = IssueCertificateModel.get_by_id(row_id)

    pkey_pem = issue_certificate_row.ssl_certificate_key
    domains = issue_certificate_row.domains

    acme_client = acme_v2_api.get_acme_client()

    # Create domain private key and CSR
    pkey_pem, csr_pem = acme_v2_api.new_csr_comp(domains, pkey_pem)

    orderr = acme_client.new_order(csr_pem)

    # Select HTTP-01 within offered challenges by the CA server
    challb = acme_v2_api.select_http01_chall(orderr)

    response, validation = challb.response_and_validation(acme_client.net.key)

    # Let the CA server know that we are ready for the challenge.
    acme_client.answer_challenge(challb, response)

    count = 0
    max_count = 5

    while True:
        count += 1

        status = get_challenge_status(issue_certificate_row.status_url)

        if status == 'valid':
            IssueCertificateModel.update(
                status=status,
                update_time=datetime_util.get_datetime()
            ).where(
                IssueCertificateModel.id == issue_certificate_row.id
            ).execute()

            break

        if count >= max_count:
            raise AppException("验证失败")

        time.sleep(count)


def renew_certificate(row_id):
    """
    Renew certificate
    :param row_id:
    :return:
    """
    issue_certificate_row = IssueCertificateModel.get_by_id(row_id)

    status = get_challenge_status(issue_certificate_row.status_url)

    if status != 'valid':
        raise AppException("域名未验证")

    pkey_pem = issue_certificate_row.ssl_certificate_key
    domains = issue_certificate_row.domains

    acme_client = acme_v2_api.get_acme_client()

    # Create domain private key and CSR
    pkey_pem, csr_pem = acme_v2_api.new_csr_comp(domains, pkey_pem)

    orderr = acme_client.new_order(csr_pem)

    # Select HTTP-01 within offered challenges by the CA server
    challb = acme_v2_api.select_http01_chall(orderr)
    logger.debug(challb.to_json())

    # Performing challenge

    fullchain_pem = acme_v2_api.perform_http01(acme_client, challb, orderr)

    logger.debug(fullchain_pem)

    fullchain_com = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM, fullchain_pem
    )

    cert = cert_common.parse_cert(fullchain_com)

    IssueCertificateModel.update(
        ssl_certificate=fullchain_pem,
        status='valid',
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
    res = requests.get(url)

    data = res.json()
    logger.debug(data)

    return data['status']
