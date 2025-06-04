"""
@File    : check_wechat_api.py
@Date    : 2025-06-04
"""
from flask import request

from domain_admin.enums.role_enum import RoleEnum
from domain_admin.service import auth_service
from domain_admin.utils import wechat_util


@auth_service.permission(role=RoleEnum.USER)
def validate_url_for_wechat():
    url = request.json['url']
    return wechat_util.validate_url_for_wechat(url)
