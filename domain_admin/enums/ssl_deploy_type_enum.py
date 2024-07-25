# -*- coding: utf-8 -*-
"""
@File    : ssl_deploy_type_enum.py
@Date    : 2024-06-27
"""


class SSLDeployTypeEnum(object):
    """
    ssl证书部署方式
    """
    SSH = 0

    WEB_HOOK = 1

    OSS = 2

    CDN = 3

    DCDN = 4
