# -*- coding: utf-8 -*-
from datetime import datetime

from flask.json.provider import DefaultJSONProvider, _default as __default
from peewee import ModelSelect

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def _default(o):
    if isinstance(o, ModelSelect):
        return list(o.dicts())

    if isinstance(o, datetime):
        return o.strftime(DATETIME_FORMAT)

    return __default(o)


class JSONProvider(DefaultJSONProvider):
    default = staticmethod(_default)
