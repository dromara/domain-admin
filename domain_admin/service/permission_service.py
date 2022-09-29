# -*- coding: utf-8 -*-
from flask import request, g

from domain_admin.service import token_service
from domain_admin.utils.flask_ext.app_exception import AppException, UnauthorizedAppException

# 白名单
WHITE_LIST = [
    '/api/login',
    '/api/register'
]

API_PREFIX = '/api'

TOKEN_KEY = 'X-Token'


def check_permission():
    if not request.path.startswith(API_PREFIX):
        return

    if request.path in WHITE_LIST:
        return

    token = request.headers.get(TOKEN_KEY)

    if not token:
        raise UnauthorizedAppException()

    try:

        payload = token_service.decode_token(token)
        g.user_id = payload['user_id']

    except Exception:
        raise AppException('token无效')
