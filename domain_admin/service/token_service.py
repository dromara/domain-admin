# -*- coding: utf-8 -*-
"""
token_service.py
"""

from datetime import datetime, timedelta

import jwt

from domain_admin.service import system_service
from domain_admin.utils.flask_ext.app_exception import AppException, ForbiddenAppException


def encode_token(payload):
    """
    获取token
    :param payload: dict
    :return: byte
    """
    config = system_service.get_system_config()
    secret_key = config['secret_key']
    token_expire_days = int(config['token_expire_days'])

    # 使用utc时间
    payload['exp'] = datetime.utcnow() + timedelta(days=token_expire_days)

    # 返回 str 部分Python版本会报错
    return jwt.encode(payload=payload, key=secret_key, algorithm='HS256')


def decode_token(token):
    """
    验证并解析token
    :param token: str
    :return:  dict
    """
    config = system_service.get_system_config()

    secret_key = config['secret_key']
    try:
        return jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'])
    except Exception:
        raise ForbiddenAppException()


if __name__ == '__main__':
    data = {'name': 'Tom'}
    w = encode_token(data)
    print(w)

    print(decode_token(w))
