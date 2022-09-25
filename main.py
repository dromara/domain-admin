# -*- coding: utf-8 -*-
"""
生产环境启动入口
"""

from werkzeug.middleware.proxy_fix import ProxyFix

from domain_admin.app import app

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(port=9090, host="0.0.0.0")
