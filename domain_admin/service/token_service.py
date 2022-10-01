# -*- coding: utf-8 -*-
"""
token_service.py
"""

from datetime import datetime, timedelta

import jwt

from domain_admin.config import SECRET_KEY, TOKEN_EXPIRE_DAYS
from domain_admin.utils.flask_ext.app_exception import AppException


def encode_token(payload):
    """
    获取token
    :param payload: dict
    :return: byte
    """

    # 使用utc时间
    payload['exp'] = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)

    # 返回 str 部分Python版本会报错
    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256')


def decode_token(token):
    """
    验证并解析token
    :param token: str
    :return:  dict
    """
    try:
        return jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    except Exception:
        raise AppException('token无效')


if __name__ == '__main__':
    data = {'name': 'Tom'}
    w = encode_token(data)
    print(w)

    print(decode_token(w))
