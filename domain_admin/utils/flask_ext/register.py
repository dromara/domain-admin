# -*- coding: utf-8 -*-


def register_app_routers(app, routers):
    """注册路由函数"""
    for url, func in routers.items():
        app.add_url_rule(url, None, func, methods=['POST', 'GET'])
