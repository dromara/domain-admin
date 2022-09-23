# -*- coding: utf-8 -*-


class AppException(Exception):
    def __init__(self, message, code=-1):
        super().__init__()

        self.code = code
        self.message = message
