# -*- coding: utf-8 -*-
from domain_admin.utils.flask_ext.handler import error_handler


def register_app_routers(app, routers):
    """注册路由函数"""
    for url, func in routers.items():
        app.add_url_rule(url, None, func, methods=['POST', 'GET'])


def register_error_handler(app):
    """
    全局异常捕获，也相当于一个视图函数
    """
    app.register_error_handler(Exception, error_handler)
