# -*- coding: utf-8 -*-

from collections import Iterator

from flask import Flask
from peewee import ModelSelect, Model
from playhouse.shortcuts import model_to_dict

from domain_admin.utils.flask_ext.api_result import ApiResult
from domain_admin.utils.flask_ext.json.json_encoder import JSONEncoder
from domain_admin.utils.flask_ext.json.json_provider import JSONProvider
from domain_admin.utils.flask_ext.request import Request


class FlaskApp(Flask):
    """
    扩展Flask
    """
    # Flask <=2.0.0
    json_encoder = JSONEncoder

    # Flask > 2.0.0
    json_provider_class = JSONProvider

    request_class = Request

    def make_response(self, rv):

        if isinstance(rv, ModelSelect):
            rv = list(rv.dicts())

        if isinstance(rv, Model):
            rv = model_to_dict(rv)

        if isinstance(rv, Iterator):
            rv = list(rv)

        if isinstance(rv, (list, dict, int, str)) or rv is None:
            rv = ApiResult.success(rv)

        if isinstance(rv, ApiResult):
            rv = rv.to_dict()

        return super().make_response(rv)
