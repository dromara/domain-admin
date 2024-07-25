# -*- coding: utf-8 -*-
"""
aliyun_dcdn_api.py
"""
# This file is auto-generated, don't edit it. Thanks.

from alibabacloud_dcdn20180115 import models as dcdn_20180115_models
from alibabacloud_dcdn20180115.client import Client as dcdn20180115Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models


def set_dcdn_domain_ssl_certificate(
        access_key_id, access_key_secret,
        domain_name,
        certificate, private_key):
    """
    https://api.aliyun.com/api/dcdn/2018-01-15/SetDcdnDomainSSLCertificate?spm=api-workbench.API%20Document.0.0.26c93c7bP4PZn9&tab=DOC&lang=PYTHON&params={%22DomainName%22:%22www%22,%22SSLProtocol%22:%22on%22,%22SSLPub%22:%22xxx%22,%22SSLPri%22:%22xxx%22}
    """
    # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
    # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
    config = open_api_models.Config(
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
        access_key_id=access_key_id,
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
        access_key_secret=access_key_secret
    )
    # Endpoint 请参考 https://api.aliyun.com/product/dcdn
    config.endpoint = 'dcdn.aliyuncs.com'
    client = dcdn20180115Client(config)

    set_dcdn_domain_sslcertificate_request = dcdn_20180115_models.SetDcdnDomainSSLCertificateRequest(
        domain_name=domain_name,
        sslprotocol='on',
        sslpub=certificate,
        sslpri=private_key
    )
    runtime = util_models.RuntimeOptions()

    # 复制代码运行请自行打印 API 的返回值
    client.set_dcdn_domain_sslcertificate_with_options(set_dcdn_domain_sslcertificate_request, runtime)
