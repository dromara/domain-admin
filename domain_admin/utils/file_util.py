# -*- coding: utf-8 -*-
import uuid


def get_random_filename(ext):
    """
    获取一个随机文件名
    :param ext: str
    :return:
    """
    return str(uuid.uuid4()) + '.' + ext
