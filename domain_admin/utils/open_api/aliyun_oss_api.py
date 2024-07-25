# -*- coding: utf-8 -*-
"""
@File    : aliyun_oss_api.py
@Date    : 2024-02-02
@Author  : Peng Shiyu

OSS Python SDK适用于Python 2.6、2.7、3.3、3.4、3.5、3.6、3.7、3.8及以上版本。

https://help.aliyun.com/zh/oss/developer-reference/map-custom-domain-names-4?spm=a2c4g.11186623.0.i6
"""
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider, StaticCredentialsProvider

# https://next.api.aliyun.com/product/Oss
from domain_admin.utils import domain_util, dns_util

ENDPOINT_OPTIONS = [
    {
        'label': '华北1（青岛）',
        'value': 'cn-qingdao',
        'endpoint': 'https://oss-cn-qingdao.aliyuncs.com',
    },
    {
        'label': '华北2（北京）',
        'value': 'cn-beijing',
        'endpoint': 'https://oss-cn-beijing.aliyuncs.com',
    },
    {
        'label': '华北3（张家口）',
        'value': 'cn-zhangjiakou',
        'endpoint': 'https://oss-cn-zhangjiakou.aliyuncs.com',
    },
    {
        'label': '华北6（乌兰察布）',
        'value': 'cn-wulanchabu',
        'endpoint': 'https://oss-cn-wulanchabu.aliyuncs.com',
    },
    {
        'label': '华东1（杭州）',
        'value': 'cn-hangzhou',
        'endpoint': 'https://oss-cn-hangzhou.aliyuncs.com',
    },
    {
        'label': '华东2（上海）',
        'value': 'cn-shanghai',
        'endpoint': 'https://oss-cn-shanghai.aliyuncs.com',
    },
    {
        'label': '华南1（深圳）',
        'value': 'cn-shenzhen',
        'endpoint': 'https://oss-cn-shenzhen.aliyuncs.com',
    },
    {
        'label': '华南3（广州）',
        'value': 'cn-guangzhou',
        'endpoint': 'https://oss-cn-guangzhou.aliyuncs.com',
    },
    {
        'label': '西南1（成都）',
        'value': 'cn-chengdu',
        'endpoint': 'https://oss-cn-chengdu.aliyuncs.com',
    }
]


def get_endpoint_by_value(value):
    for item in ENDPOINT_OPTIONS:
        if item['value'] == value:
            return item['endpoint']


def cname_to_oss_info(cname):
    """
    'zaiting.oss-cn-beijing.aliyuncs.com.'
    :param cname:
    :return: zaiting  oss-cn-beijing.aliyuncs.com
    """
    lst = dns_util.query_domain_cname(cname)

    if lst and len(lst) > 0:
        domain = lst[0]

        return {
            'bucket_name': domain.split('.')[0],
            'endpoint': 'https://' + domain_util.get_domain_parent(domain).strip('.')
        }
    else:
        return None


def put_bucket_cname(
        access_key_id,
        access_key_secret,
        bucket_name,
        domain,
        certificate,
        private_key,
        endpoint='https://oss-cn-beijing.aliyuncs.com',
):
    """
    将证书部署到oss
    :param access_key_id:
    :param access_key_secret:
    :param bucket_name:
    :param domain:
    :param certificate:
    :param private_key:
    :param endpoint:
    :return:
    """
    # 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
    auth = oss2.ProviderAuth(
        StaticCredentialsProvider(access_key_id=access_key_id, access_key_secret=access_key_secret)
    )

    # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # 填写Bucket名称，例如examplebucket。
    bucket = oss2.Bucket(
        auth=auth,
        # https://oss-cn-beijing.aliyuncs.com
        endpoint=endpoint,
        bucket_name=bucket_name
    )

    cert = oss2.models.CertInfo(certificate=certificate, private_key=private_key)
    # 通过force=True设置强制覆盖旧版证书。
    # 通过delete_certificate选择是否删除证书。设置为delete_certificate=True表示删除证书，设置为delete_certificate=False表示不删除证书。
    # cert = oss2.models.CertInfo(certificate=certificate, private_key=private_key, force=True, delete_certificate=False)
    input = oss2.models.PutBucketCnameRequest(domain, cert)
    bucket.put_bucket_cname(input)
