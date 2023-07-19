# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

import six
from flask import request, Response
from peewee import DoesNotExist, IntegrityError

from domain_admin.log import logger
from domain_admin.utils.flask_ext.api_result import ApiResult
import traceback

from domain_admin.utils.flask_ext.app_exception import AppException


def error_handler(e):
    """
    全局错误处理
    :param e: Exception
    :return:
    """

    logger.error(traceback.format_exc())

    if request.path.startswith('/api'):

        code = -1

        if isinstance(e, KeyError):
            msg = '参数缺失' + str(e)

        elif isinstance(e, DoesNotExist):
            msg = '数据不存在'

        elif isinstance(e, IntegrityError):
            msg = '数据已存在'

        elif isinstance(e, AppException):
            msg = e.get_message()
            code = e.get_code()

        else:
            msg = six.text_type(e)

        return ApiResult.error(msg=msg, code=code)
    else:
        return Response("Internal Server Error: {}".format(e.message), status=500)
