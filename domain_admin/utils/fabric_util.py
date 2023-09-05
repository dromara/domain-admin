# -*- coding: utf-8 -*-
"""
@File    : fabric_util.py
@Date    : 2023-07-26

参考
https://www.fabfile.org/installing.html
https://docs.fabfile.org/en/stable/api/connection.html

https://www.cnblogs.com/superhin/p/13887526.html
"""

import six
from fabric import Connection
from paramiko import RSAKey

from domain_admin.log import logger
from domain_admin.utils.flask_ext.app_exception import AppException

# 命令白名单
allow_commands = [
    # 重启nginx
    'service nginx force-reload'
]


def deploy_file(host, user, password, content, remote):
    """
    远程部署文件
    :param host:
    :param user:
    :param password:
    :param content:
    :param remote:
    :return:
    """
    logger.info(remote)

    with Connection(
            host=host,
            user=user,
            connect_kwargs={"password": password}
    ) as conn:
        conn.put(six.StringIO(content), remote)


def run_command(host, user, password, command):
    """
    远程运行命令
    :param host:
    :param user:
    :param password:
    :param command:
    :return:
    """
    logger.info(command)

    if command not in allow_commands:
        raise AppException("命令不被允许，请联系管理员")

    with Connection(
            host=host,
            user=user,
            connect_kwargs={"password": password}
    ) as conn:
        conn.run(command, hide=True)


def deploy_file_by_key(host, user, private_key, content, remote):
    """
    远程部署文件
    :param host:
    :param user:
    :param private_key:
    :param content:
    :param remote:
    :return:
    """
    logger.info(remote)

    with Connection(
            host=host,
            user=user,
            connect_kwargs={"pkey": RSAKey.from_private_key(six.StringIO(private_key))}
    ) as conn:
        conn.put(six.StringIO(content), remote)


def run_command_by_key(host, user, private_key, command):
    """
    远程运行命令
    :param password:
    :param host:
    :param user:
    :param private_key:
    :param command:
    :return:
    """
    logger.info(command)

    if command not in allow_commands:
        raise AppException("命令不被允许，请联系管理员")

    with Connection(
            host=host,
            user=user,
            connect_kwargs={"pkey": RSAKey.from_private_key(six.StringIO(private_key))}
    ) as conn:
        conn.run(command, hide=True)
