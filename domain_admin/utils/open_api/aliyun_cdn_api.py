# -*- coding: utf-8 -*-
"""
@File    : aliyun_cdn_api.py
@Date    : 2024-07-24
"""

from alibabacloud_cdn20180510 import models as cdn_20180510_models
from alibabacloud_cdn20180510.client import Client as Cdn20180510Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

from domain_admin.utils import uuid_util
from domain_admin.utils.open_api import aliyun_cas_api


def set_cdn_domain_ssl_certificate(
        access_key_id, access_key_secret,
        domain_name,
        cert_id, cert_name):
    """
    https://api.aliyun.com/api-tools/sdk/Cdn?spm=api-workbench.api_explorer.0.0.539f3761ceDHDv&version=2018-05-10&language=python-tea&tab=primer-doc
    :param access_key_id:
    :param access_key_secret:
    :param domain_name:
    :param cert_id:
    :return:
    """
    # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
    # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
    config = open_api_models.Config(
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
        access_key_id=access_key_id,
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
        access_key_secret=access_key_secret,
    )

    # Endpoint 请参考 https://api.aliyun.com/product/Cdn
    config.endpoint = 'cdn.aliyuncs.com'
    client = Cdn20180510Client(config)

    set_cdn_domain_sslcertificate_request = cdn_20180510_models.SetCdnDomainSSLCertificateRequest(
        cert_id=cert_id,
        cert_name=cert_name,
        cert_type='cas',
        domain_name=domain_name,
        sslprotocol='on'
    )
    runtime = util_models.RuntimeOptions()

    # 复制代码运行请自行打印 API 的返回值
    client.set_cdn_domain_sslcertificate_with_options(set_cdn_domain_sslcertificate_request, runtime)


def set_cdn_domain_cert(
        access_key_id, access_key_secret,
        domain,
        certificate, private_key):
    """
    先上传，再部署
    :param access_key_id:
    :param access_key_secret:
    :param domain:
    :param certificate:
    :param private_key:
    :return:
    """
    cert_name = uuid_util.get_uuid()
    cert_id = aliyun_cas_api.upload_user_certificate(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        cert_name=cert_name,
        cert=certificate,
        key=private_key
    )

    print('cert_id: ', cert_id)

    set_cdn_domain_ssl_certificate(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        domain_name=domain,
        cert_id=cert_id,
        cert_name=cert_name
    )


def set_cdn_domain_ssl_certificate_v2(
        access_key_id, access_key_secret,
        domain_name,
        certificate, private_key
):
    """
    直接部署到CDN
    https://api.aliyun.com/api-tools/sdk/Cdn?spm=api-workbench.api_explorer.0.0.539f3761ceDHDv&version=2018-05-10&language=python-tea&tab=primer-doc
    :return:
    """
    # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
    # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
    config = open_api_models.Config(
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
        access_key_id=access_key_id,
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
        access_key_secret=access_key_secret,
    )

    # Endpoint 请参考 https://api.aliyun.com/product/Cdn
    config.endpoint = 'cdn.aliyuncs.com'
    client = Cdn20180510Client(config)

    set_cdn_domain_sslcertificate_request = cdn_20180510_models.SetCdnDomainSSLCertificateRequest(
        domain_name=domain_name,
        cert_type='upload',
        sslpri=private_key,
        sslpub=certificate,
        sslprotocol='on'
    )

    runtime = util_models.RuntimeOptions()

    # 复制代码运行请自行打印 API 的返回值
    client.set_cdn_domain_sslcertificate_with_options(set_cdn_domain_sslcertificate_request, runtime)
