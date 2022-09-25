# -*- coding: utf-8 -*-

"""
$ gunicorn --config gunicorn.conf.py main:app
"""

import multiprocessing
import os

# 日志文件夹
LOG_DIR = 'logs'

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)


def resolve_file(filename):
    return os.path.join(LOG_DIR, filename)


def get_workers():
    return multiprocessing.cpu_count() * 2 + 1


# daemon = True
daemon = False  # 使用supervisor不能是后台进程

# 进程名称
proc_name = "domain-admin"

# 启动端口
bind = "127.0.0.1:9090"

# 日志文件
loglevel = 'debug'
pidfile = 'gunicorn.pid'
accesslog = resolve_file("access.log")
errorlog = resolve_file("error.log")

# 启动的进程数
# workers = get_workers()
workers = 2
worker_class = 'gevent'


# 启动时钩子
def on_starting(server):
    ip, port = server.address[0]
    print('server.address:', f'http://{ip}:{port}')
