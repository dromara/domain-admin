# -*- coding: utf-8 -*-
"""
@File    : md5_util.py
@Date    : 2023-06-30
"""
import hashlib


def md5(msg: str):
    return hashlib.md5(msg.encode("utf-8")).hexdigest()
