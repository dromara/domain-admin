# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

import six
from flask import Flask, Response
from peewee import ModelSelect, Model

from domain_admin.compat import Iterator
from domain_admin.utils.flask_ext.api_result import ApiResult
from domain_admin.utils.flask_ext.request import Request


class FlaskApp(Flask):
    """
    扩展Flask
    """
    # Flask <=2.0.0
    # json_encoder = JSONEncoder

    # Flask > 2.0.0
    # json_provider_class = JSONProvider

    request_class = Request

    # 需要转为json的类型
    json_data_class = (
        ModelSelect,
        Model,
        Iterator,
        list,
        dict,
        six.integer_types,
        six.text_type
    )

    def make_response(self, rv):

        if isinstance(rv, self.json_data_class) or rv is None:
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
