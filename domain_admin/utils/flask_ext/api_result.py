# -*- coding: utf-8 -*-


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
