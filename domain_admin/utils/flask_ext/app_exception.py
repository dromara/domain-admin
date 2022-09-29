# -*- coding: utf-8 -*-
from domain_admin.utils.flask_ext.http_code_enum import HttpCodeEnum


class AppException(Exception):
    def __init__(self, message, code=-1):
        super().__init__()

        self.code = code
        self.message = message


class ForbiddenAppException(AppException):
    def __init__(self, message='暂无权限', code=HttpCodeEnum.Forbidden):
        super().__init__(message, code)


class UnauthorizedAppException(AppException):
    def __init__(self, message='用户未登录', code=HttpCodeEnum.Unauthorized):
        super().__init__(message, code)
