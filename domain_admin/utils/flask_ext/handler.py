# -*- coding: utf-8 -*-
from domain_admin.utils.flask_ext.api_result import ApiResult


def error_handler(e):
    return ApiResult.error(msg=str(e))
