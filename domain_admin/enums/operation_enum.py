# -*- coding: utf-8 -*-
"""
@File    : status_enum.py
@Date    : 2022-10-30
@Author  : Peng Shiyu
"""
from __future__ import print_function, unicode_literals, absolute_import, division

class OperationEnum(object):
    """
    数据操作枚举值
    """

    # 添加
    CREATE = 1

    # 更新
    UPDATE = 2

    # 删除
    DELETE = 3

    # 批量删除
    BATCH_DELETE = 4

    @staticmethod
    def get_label(value):
        mapping = {
            OperationEnum.CREATE: '添加',
            OperationEnum.UPDATE: '更新',
            OperationEnum.DELETE: '删除',
            OperationEnum.BATCH_DELETE: '批量删除',

        }

        return mapping.get(value)
