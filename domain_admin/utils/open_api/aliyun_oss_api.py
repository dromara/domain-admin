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


def create_bucket_cname_token():
    # 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
    auth = oss2.ProviderAuth(StaticCredentialsProvider(access_key_id="", access_key_secret="", security_token=""))

    # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # 填写Bucket名称，例如examplebucket。
    bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'examplebucket')

    # 填写自定义域名。
    test_domain = 'www.example.com'
    # 创建CnameToken。
    result = bucket.create_bucket_cname_token(test_domain)
    # 打印绑定的Cname名称。
    print(result.cname)
    # 打印OSS返回的CnameToken。
    print(result.token)
    # 打印CnameToken的过期时间。
    print(result.expire_time)


def put_bucket_cname():
    # 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
    auth = oss2.ProviderAuth(StaticCredentialsProvider(access_key_id="", access_key_secret="", security_token=""))

    # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # 填写Bucket名称，例如examplebucket。
    bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'examplebucket')

    # 填写自定义域名。
    test_domain = 'www.example.com'
    # 填写旧版证书ID。
    previous_cert_id = '001'
    certificate = '''-----BEGIN CERTIFICATE-----
    MIIDWzCCAkOgA******KTgnwyOGU9cv+mxA=
    -----END CERTIFICATE-----'''
    # 设置证书私钥。
    private_key = '''-----BEGIN PRIVATE KEY-----
    MIIEvQIBADAN******1i2t41Q/SC3HUGC5mJjpO8=
    -----END PRIVATE KEY-----
    '''

    cert = oss2.models.CertInfo(certificate=certificate, private_key=private_key)
    # 通过force=True设置强制覆盖旧版证书。
    # 通过delete_certificate选择是否删除证书。设置为delete_certificate=True表示删除证书，设置为delete_certificate=False表示不删除证书。
    # cert = oss2.models.CertInfo(certificate=certificate, private_key=private_key, force=True, delete_certificate=False)
    input = oss2.models.PutBucketCnameRequest(test_domain, cert)
    bucket.put_bucket_cname(input)
