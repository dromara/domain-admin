# -*- coding: utf-8 -*-
from flask import Request as _Request


class Request(_Request):
    @property
    def json(self):
        """
        强制返回json
        :return:
        """
        return self.get_json(force=True)
