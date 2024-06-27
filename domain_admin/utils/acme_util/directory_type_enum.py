# -*- coding: utf-8 -*-
"""
@File    : directory_type_enum.py
@Date    : 2024-06-27
"""


class DirectoryTypeEnum(object):
    """
    证书签发提供商
    """
    LETS_ENCRYPT = 'letsencrypt'

    LETS_ENCRYPT_STAGING = 'letsencrypt-staging'

    ZERO_SSL = 'zerossl'

    GOOGLE = 'google'


# 证书签发提供商
DIRECTORY_URL_OPTIONS = [
    {
        'label': "LetsEncrypt",
        'value': DirectoryTypeEnum.LETS_ENCRYPT,
        'directory_url': "https://acme-v02.api.letsencrypt.org/directory",
    },
    {
        'label': "LetsEncrypt-Staging",
        'value': DirectoryTypeEnum.LETS_ENCRYPT_STAGING,
        'directory_url': 'https://acme-staging-v02.api.letsencrypt.org/directory',
    },
    {
        'label': "ZeroSSL",
        'value': DirectoryTypeEnum.ZERO_SSL,
        'directory_url': "https://acme.zerossl.com/v2/DV90/directory",
    },
    {
        'label': "Google",
        'value': DirectoryTypeEnum.GOOGLE,
        'directory_url': "https://dv.acme-v02.api.pki.goog/directory",
    },
]


def get_directory_url_option(directory_type):
    for item in DIRECTORY_URL_OPTIONS:
        if item['value'] == directory_type:
            return item


def get_directory_url(directory_type):
    item = get_directory_url_option(directory_type)
    if item:
        return item['directory_url']
