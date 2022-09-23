# -*- coding: utf-8 -*-
from werkzeug.middleware.proxy_fix import ProxyFix

from domain_admin.app import app

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(port=8080, host="0.0.0.0")
