# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

from concurrent.futures.thread import ThreadPoolExecutor

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
    executor.submit(fn, *args, **kwargs)
