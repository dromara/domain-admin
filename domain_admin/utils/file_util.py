# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division
import uuid


def get_random_filename(ext):
    """
    获取一个随机文件名
    :param ext: str
    :return:
    """
    return str(uuid.uuid4()) + '.' + ext


def get_filename_ext(filename):
    """
    获取文件名的扩展名
    :param filename:
    :return:
    """
    return filename.split('.')[-1]
