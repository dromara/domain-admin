# -*- coding: utf-8 -*-
from flask import request, make_response
from flask_cors import CORS

from domain_admin.model import db
from domain_admin.router import routes
from domain_admin.utils.flask_ext.flask_app import FlaskApp
from domain_admin.utils.flask_ext.register import register_app_routers, register_error_handler

app = FlaskApp(__name__, static_folder=None)

CORS(app, supports_credentials=True)

# 路由
register_app_routers(app, routes)

# 异常处理
register_error_handler(app)


@app.before_request
def before_request():
    """跨域请求会出现options，直接返回即可"""
    if request.method == 'OPTIONS':
        return make_response()

    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
