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
import paramiko

from domain_admin.config import DEFAULT_SSH_PORT, ALLOW_COMMANDS
from domain_admin.log import logger
from domain_admin.utils.flask_ext.app_exception import AppException

# 命令白名单
allow_commands = [
    # 重启nginx
    'service nginx force-reload',
    # docker 下的重启命令 @since 1.5.30
    'docker exec -id nginx nginx -s reload',
    # 红帽系reload @since 1.5.31
    'systemctl reload nginx',
    'systemctl reload openresty',

    # 用户自定义配置的命令
    *ALLOW_COMMANDS,
]


def deploy_file(host, user, password, content, remote, port=DEFAULT_SSH_PORT):
    """
    远程部署文件
    :param port: 端口号
    :param host: 地址
    :param user: 用户名
    :param password: 密码
    :param content: 文件内容
    :param remote: 远程路径
    :return:
    """
    logger.info(remote)

    with Connection(
            host=host,
            port=port,
            user=user,
            connect_kwargs={"password": password}
    ) as conn:
        conn.put(six.StringIO(content), remote)


def run_command(host, user, password, command, port=DEFAULT_SSH_PORT):
    """
    远程运行命令
    :param port: 端口号
    :param host: 地址
    :param user: 用户名
    :param password: 密码
    :param command: 执行命令
    :return:
    """
    logger.info(command)

    if command not in allow_commands:
        raise AppException("命令不被允许，请联系管理员")

    with Connection(
            host=host,
            port=port,
            user=user,
            connect_kwargs={"password": password}
    ) as conn:
        conn.run(command, hide=True)


def deploy_file_by_key(host, user, private_key, content, remote, port=DEFAULT_SSH_PORT):
    """
    远程部署文件
    :param port: 端口号
    :param host: 地址
    :param user: 用户名
    :param private_key: 私钥
    :param content: 文件内容
    :param remote: 远程路径
    :return:
    """
    logger.info(remote)

    with Connection(
            host=host,
            port=port,
            user=user,
            connect_kwargs={"pkey": _get_paramiko_key(private_key)}
    ) as conn:
        conn.put(six.StringIO(content), remote)


def run_command_by_key(host, user, private_key, command, port=DEFAULT_SSH_PORT):
    """
    远程运行命令
    :param port: 端口号
    :param host: 地址
    :param user: 用户名
    :param private_key: 私钥
    :param command: 命令
    :return:
    """
    logger.info(command)

    if command not in allow_commands:
        raise AppException("命令不被允许，请联系管理员")

    with Connection(
            host=host,
            port=port,
            user=user,
            connect_kwargs={"pkey": _get_paramiko_key(private_key)}
    ) as conn:
        conn.run(command, hide=True)

def _get_paramiko_key(raw_key_content):
    """
    获取paramiko对象秘钥
    :param raw_key_content: 原始秘钥内容
    :return: paramiko 秘钥
    """
    pkey = None
    for pkey_class in (paramiko.RSAKey, paramiko.DSSKey, paramiko.ECDSAKey, paramiko.Ed25519Key):
        try:
            pkey = pkey_class.from_private_key(six.StringIO(raw_key_content))
            break
        except paramiko.SSHException as e:
            pass

    return pkey
