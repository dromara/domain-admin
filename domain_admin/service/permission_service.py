# -*- coding: utf-8 -*-
from flask import request, g

from domain_admin.config import ROOT_USERNAME
from domain_admin.model import UserModel
from domain_admin.service import token_service
from domain_admin.utils.flask_ext.app_exception import AppException, UnauthorizedAppException, ForbiddenAppException

# 白名单
WHITE_LIST = [
    '/api/login',
    '/api/register'
]

# 仅管理账号可访问的接口
ROOT_API_LIST = [

]

API_PREFIX = '/api'

TOKEN_KEY = 'X-Token'


def check_permission():
    # 仅校验api
    if not request.path.startswith(API_PREFIX):
        return

    # 白名单直接通过
    if request.path in WHITE_LIST:
        return

    # 获取token
    token = request.headers.get(TOKEN_KEY)

    if not token:
        raise UnauthorizedAppException()

    # 解析token
    payload = token_service.decode_token(token)
    g.user_id = payload['user_id']

    # root 权限 api
    if request.path in ROOT_API_LIST:
        user_row = UserModel.get_by_id(g.user_id)

        if user_row.username != ROOT_USERNAME:
            raise ForbiddenAppException()
