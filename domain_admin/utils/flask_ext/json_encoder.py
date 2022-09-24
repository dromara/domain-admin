# -*- coding: utf-8 -*-
from datetime import datetime

from flask.json import JSONEncoder as _JSONEncoder
from peewee import ModelSelect, Model
from playhouse.shortcuts import model_to_dict


class JSONEncoder(_JSONEncoder):
    """ flask == 0.1 """
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def default(self, o):
        if isinstance(o, ModelSelect):
            return list(o.dicts())

        if isinstance(o, Model):
            return model_to_dict(o)

        if isinstance(o, datetime):
            return o.strftime(self.DATETIME_FORMAT)

        return super().default(o)
