# -*- coding: utf-8 -*-

"""
生产环境
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


# 启动端口
bind = "0.0.0.0:9090"

# 日志文件
loglevel = 'debug'
pidfile = 'gunicorn.pid'
accesslog = resolve_file("gunicorn-access.log")
errorlog = resolve_file("gunicorn-error.log")

# 启动的进程数
# workers = get_workers()

# 需要定时器，只能开一个进程
workers = 1
worker_class = 'gevent'


# 启动时钩子
def on_starting(server):
    ip, port = server.address[0]
    print('server.address:', f'http://{ip}:{port}')
