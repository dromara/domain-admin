# -*- coding: utf-8 -*-
"""
@File    : util.py
@Date    : 2023-03-25
"""
import socket


def parse_whois_raw(whois_raw: str):
    """
    解析键值对
    :param whois_raw:
    :return:
    """
    data = {}
    for row in whois_raw.split("\n"):
        row_split = row.split(":", maxsplit=1)
        if len(row_split) == 2:
            key, value = row_split
            data[key.strip()] = value.strip()

    return data


def get_whois_raw(domain: str, server: str, port=43, timeout=5) -> str:
    """
    发送http请求，获取信息
    :param domain:
    :param server:
    :param port:
    :return:
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
