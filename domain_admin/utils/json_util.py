# -*- coding: utf-8 -*-
"""
@File    : json_util.py
@Date    : 2023-04-16
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import json
from datetime import datetime
from domain_admin.compat import Iterator
from acme.messages import ChallengeBody
from peewee import ModelSelect, Model
from playhouse.shortcuts import model_to_dict

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def default_json_encoder(o):
    """
    json 序列化
    :param o:
    :return:
    """

    if isinstance(o, ModelSelect):
        return list(o.dicts())

    if isinstance(o, Model):
        return model_to_dict(o)

    if isinstance(o, Iterator):
        return list(o)

    if isinstance(o, datetime):
        return o.strftime(DATETIME_FORMAT)

    if isinstance(o, ChallengeBody):
        return o.to_json()

    return o


def json_encode(data, default=default_json_encoder, **kwargs):
    """
    json序列化
    :param data:
    :param default:
    :param kwargs:
    :return:
    """
    return json.dumps(data, default=default, **kwargs)


def json_dump(obj):
    return json_encode(obj, ensure_ascii=False, indent=2)
