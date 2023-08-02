# -*- coding: utf-8 -*-
"""
@File    : dev.py
@Date    : 2023-06-14

启动方式
$ flask run
"""
from domain_admin.main import app

if __name__ == '__main__':
    app.run(port=8000)
