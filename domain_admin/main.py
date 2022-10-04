# -*- coding: utf-8 -*-
import os

from flask import request, make_response, send_file
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import safe_join
from domain_admin.config import TEMP_DIR
from domain_admin.model.base_model import db
from domain_admin.model.database import init_database
from domain_admin.router import api_map, permission
from domain_admin.service import scheduler_service
from domain_admin.utils.flask_ext import handler
from domain_admin.utils.flask_ext import register
from domain_admin.utils.flask_ext.flask_app import FlaskApp

app = FlaskApp(__name__,
               static_folder="public",
               static_url_path="/"
               )


@app.before_request
def before_request():
    """跨域请求会出现options，直接返回即可"""
    if request.method == 'OPTIONS':
        return make_response()

    permission.check_permission()

    db.connect(reuse_if_open=True)


@app.teardown_request
def teardown_request(exc):
    if not db.is_closed():
        db.close()


@app.get('/')
def index():
    return send_file('public/index.html')


@app.get('/temp/<path:filename>')
def temp(filename):
    """临时文件"""
    return send_file(safe_join(TEMP_DIR, filename))


def app_init(app):
    # 路由
    register.register_app_routers(app, api_map.routes)

    # 全局异常捕获，也相当于一个视图函数
    app.register_error_handler(Exception, handler.error_handler)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    CORS(app, supports_credentials=True)

    init_database()

    scheduler_service.init_scheduler()


app_init(app)
