# -*- coding: utf-8 -*-
from peewee import DoesNotExist

from domain_admin.utils.flask_ext.api_result import ApiResult
import traceback


def error_handler(e):
    traceback.print_exc()

    if isinstance(e, KeyError):
        msg = '参数缺失' + str(e)

    elif isinstance(e, DoesNotExist):
        msg = '数据不存在'

    else:
        msg = str(e)

    return ApiResult.error(msg=msg)
