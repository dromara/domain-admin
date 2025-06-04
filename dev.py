# -*- coding: utf-8 -*-
"""
@File    : dev.py
@Date    : 2023-06-14
"""
from domain_admin.main import app

if __name__ == '__main__':
    app.run(debug=True, port=5001)
