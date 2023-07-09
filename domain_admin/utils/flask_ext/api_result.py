# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.utils import json_util


class ApiResult(object):
    """返回统一的数据结构"""

    def __init__(self, data, msg, code):
        self.data = data
        self.msg = msg
        self.code = code

    @classmethod
    def success(cls, data=None, msg='success', code=0):
        return cls(data, msg, code)

    @classmethod
    def error(cls, data=None, msg='error', code=-1):
        return cls(data, msg, code)

    def to_dict(self):
        return {
            'data': self.data,
            'code': self.code,
            'msg': self.msg
        }

    def to_json(self):
        return json_util.json_encode(self.to_dict())
