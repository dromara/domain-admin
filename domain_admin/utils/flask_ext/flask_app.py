# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

from domain_admin.compat import Iterator

import six

from flask import Flask, Response
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

        if isinstance(rv, (list, dict, six.integer_types, six.text_type)) or rv is None:
            rv = ApiResult.success(rv)

        if isinstance(rv, ApiResult):
            return Response(rv.to_json(), content_type='application/json;charset=utf-8')

        return super(FlaskApp, self).make_response(rv)

    def get(self, rule, **options):
        options.setdefault('methods', ['GET'])
        return super(FlaskApp, self).route(rule, **options)

    def post(self, rule, **options):
        options.setdefault('methods', ['POST'])
        return super(FlaskApp, self).route(rule, **options)
