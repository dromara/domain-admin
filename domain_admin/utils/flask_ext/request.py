# -*- coding: utf-8 -*-
from flask import Request as _Request


class Request(_Request):
    @property
    def json(self):
        data = self.get_json()

        if not data:
            data = {}

        return data
