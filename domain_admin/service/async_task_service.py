# -*- coding: utf-8 -*-
"""
异步任务
async_task_service.py
"""

from __future__ import print_function, unicode_literals, absolute_import, division

import traceback
from functools import wraps

import six
from concurrent.futures.thread import ThreadPoolExecutor
from flask import g

from domain_admin.log import logger
from domain_admin.model.log_async_task_model import AsyncTaskModel
from domain_admin.utils import datetime_util

executor = ThreadPoolExecutor()


def submit_task(fn, *args, **kwargs):
    """
    执行异步任务
    see:
    https://pengshiyu.blog.csdn.net/article/details/114700730
    :param fn:
    :param args:
    :param kwargs:
    :return:
    """
    return executor.submit(fn, *args, **kwargs)


def async_task_decorator(task_name):
    """
    执行异步任务的装饰器
    :param task_name:
    :return:
    """

    def outer_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user_id = g.user_id

            # before
            async_task_row = AsyncTaskModel.create(
                user_id=current_user_id,
                task_name=task_name,
                function_name="{}.{}".format(func.__module__, func.__name__),
                start_time=datetime_util.get_datetime()
            )

            # callback
            def done_callback(future):

                is_success = None
                result = ''

                try:
                    result = future.result()
                    is_success = True
                except Exception as e:
                    is_success = False
                    result = e
                    logger.error(traceback.format_exc())

                if result:
                    result = six.text_type(result)
                else:
                    result = ''

                data = {
                    'status': is_success,
                    'result': result,
                    'end_time': datetime_util.get_datetime(),
                    'update_time': datetime_util.get_datetime(),
                }

                AsyncTaskModel.update(data).where(
                    AsyncTaskModel.id == async_task_row.id
                ).execute()

            # execute
            ret = submit_task(func, *args, **kwargs)

            # after
            ret.add_done_callback(done_callback)

            return ret

        return wrapper

    return outer_wrapper
