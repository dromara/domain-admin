# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division


from flask import request, make_response, send_file
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from domain_admin import compat
from domain_admin.config import TEMP_DIR
from domain_admin.model.base_model import db
from domain_admin.model.database import init_database
from domain_admin.router import api_map, permission
from domain_admin.service import scheduler_service, system_service
from domain_admin.service import version_service
from domain_admin.utils.flask_ext import handler
from domain_admin.utils.flask_ext import register
from domain_admin.utils.flask_ext.flask_app import FlaskApp

app = FlaskApp(
    import_name=__name__,
    static_folder="public",
    static_url_path="/"
)


@app.before_request
def before_request():
    """跨域请求会出现options，直接返回即可"""
    if request.method == 'OPTIONS':
        response = make_response()
        # 响应的有效时间，单位是【秒】
        response.headers.set('Access-Control-Max-Age', 60 * 30)
        return response

    permission.check_permission()

    db.connect(reuse_if_open=True)


@app.teardown_request
def teardown_request(exc):
    if not db.is_closed():
        db.close()


@app.get('/')
def index():
    """
    静态首页
    :return:
    """
    return send_file('public/index.html')


@app.get('/m/')
def mobile():
    """
    移动端首页
    :return:
    """
    return send_file('public/m/index.html')


@app.get('/test')
def app_hello():
    """
    测试页
    :return:
    """
    return 'hello'


@app.get('/temp/<path:filename>')
def temp(filename):
    """临时文件"""
    return send_file(compat.safe_join(TEMP_DIR, filename))


def init_app(flask_app):
    """
    初始化app
    :param flask_app:
    :return:
    """

    # 注册路由
    register.register_app_routers(flask_app, api_map.routes)

    # 全局异常捕获，也相当于一个视图函数
    flask_app.register_error_handler(Exception, handler.error_handler)

    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)

    # 允许跨域
    CORS(flask_app, supports_credentials=True)

    # 初始化数据库
    init_database()

    # fixed: peewee.OperationalError: no such table: tb_version
    # ref: https://github.com/coleifer/peewee/issues/2095
    # 初始化完数据库和表之后等待写入完成
    # time.sleep(0.01)

    # 版本自动升级
    version_service.update_version()

    # 启动定时器
    scheduler_service.init_scheduler()

    # 初始化全局常量配置
    system_service.init_system_config(flask_app)


init_app(app)
