# -*- coding: utf-8 -*-
from peewee import DoesNotExist, IntegrityError

from domain_admin.log import logger
from domain_admin.utils.flask_ext.api_result import ApiResult
import traceback

from domain_admin.utils.flask_ext.app_exception import AppException


def error_handler(e):
    """
    全局错误处理
    :param e:
    :return:
    """
    # traceback.print_exc()
    logger.error(traceback.format_exc())

    code = -1

    if isinstance(e, KeyError):
        msg = '参数缺失' + str(e)

    elif isinstance(e, DoesNotExist):
        msg = '数据不存在'

    elif isinstance(e, IntegrityError):
        msg = '数据已存在'

    elif isinstance(e, AppException):
        msg = e.message
        code = e.code

    else:
        msg = str(e)

    return ApiResult.error(msg=msg, code=code)
