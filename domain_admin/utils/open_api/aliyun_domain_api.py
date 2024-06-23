# -*- coding: utf-8 -*-
"""
@File    : aliyun_domain_api.py
@Date    : 2024-06-17
"""

from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.client import AcsClient

from domain_admin.log import logger


class RecordTypeEnum:
    """
    记录类型枚举
    ref: https://help.aliyun.com/zh/dns/dns-record-types
    """
    A = 'A'
    TXT = 'TXT'


def add_domain_record(
        access_key_id, access_key_secret,
        domain_name, record_key, record_type, record_value
):
    """
    添加域名解析记录
    doc:
    https://next.api.aliyun.com/api-tools/sdk/Alidns?version=2015-01-09&language=python&tab=primer-doc
    https://next.api.aliyun.com/api/Alidns/2015-01-09/AddDomainRecord?sdkStyle=old&tab=DEMO&lang=PYTHON


    :param access_key_id: key
    :param access_key_secret: secret
    :param domain_name: 域名名称
    :param record_key: 主机记录
    :param record_type: 解析记录类型 RecordTypeEnum
    :param record_value: 记录值
    :return:
    """
    logger.info("%s", {
        'access_key_id': access_key_id,
        'access_key_secret': access_key_secret,
        'domain_name': domain_name,
        'record_key': record_key,
        'record_type': record_type,
        'record_value': record_value,
    })

    # Please ensure that the environment variables ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are set.
    credentials = AccessKeyCredential(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret
    )

    # use STS Token
    # credentials = StsTokenCredential(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'], os.environ['ALIBABA_CLOUD_SECURITY_TOKEN'])
    client = AcsClient(region_id='cn-beijing', credential=credentials)

    request = AddDomainRecordRequest()
    request.set_accept_format('json')

    request.set_DomainName(domain_name)
    request.set_RR(record_key)
    request.set_Type(record_type)
    request.set_Value(record_value)

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))
