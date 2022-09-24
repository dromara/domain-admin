# -*- coding: utf-8 -*-
"""
开发环境启动入口
"""

from domain_admin.app import app

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
