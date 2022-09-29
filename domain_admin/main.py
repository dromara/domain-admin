# -*- coding: utf-8 -*-
"""
生产环境启动入口
"""

from domain_admin.app import app
from domain_admin.config import FLASK_HOST, FLASK_PORT

if __name__ == '__main__':
    app.run(port=FLASK_PORT, host=FLASK_HOST)
