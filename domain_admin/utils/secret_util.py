# -*- coding: utf-8 -*-
"""
secret_util.py
"""
from __future__ import print_function, unicode_literals, absolute_import, division

try:
    # @since Python3.6
    import secrets
except ImportError:
    secrets = None

import os
import base64


def get_random_secret():
    if secrets:
        return secrets.token_hex()
    else:
        # 生成32位随机字符 编码为base64
        return base64.b64encode(os.urandom(32))


if __name__ == '__main__':
    print(get_random_secret())
