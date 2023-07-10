# -*- coding: utf-8 -*-
"""
@File    : util.py
@Date    : 2023-03-25
"""
from __future__ import print_function, unicode_literals, absolute_import, division

import socket
from os import path
import io


def parse_whois_raw(whois_raw):
    """
    解析键值对
    :param whois_raw: str
    :return:
    """
    data = {}
    for row in whois_raw.split("\n"):
        # tw
        if 'Record expires on' in row or 'Record created on' in row:
            row_split = row.split("on", maxsplit=1)
        elif ":" in row:
            # fix: Python2 split() takes no keyword arguments
            row_split = row.split(":", 1)
        else:
            row_split = row.split(" ", 1)

        if len(row_split) == 2:
            key, value = row_split
            data[key.strip()] = value.strip()

    return data


def get_whois_raw(domain, server, port=43, timeout=5):
    """
    发送http请求，获取信息
    :param domain: str
    :param server: str
    :param port: int
    :param timeout: int
    :return: str
    """
    # 创建连接
    sock = socket.create_connection((server, port))
    sock.settimeout(timeout)

    # 发送请求
    sock.send(("%s\r\n" % domain).encode("utf-8"))

    # 接收数据
    buff = bytes()
    while True:
        data = sock.recv(1024)
        if len(data) == 0:
            break
        buff += data

    # 关闭链接
    sock.close()

    return buff.decode("utf-8")


def load_whois_servers():
    """
    加载域名查询服务器配置
    :return: dict {
        root: server
        ...
    }
    """
    dct = {}
    # fix：Python2 encoding error
    with io.open(path.join(path.dirname(__file__), 'whois-servers.txt'), 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith(";"):
                pass

            split_line = line.split(" ")

            if len(split_line) == 2:
                root, server = split_line
                dct[root.strip()] = server.strip()

    return dct
