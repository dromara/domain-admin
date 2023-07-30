# -*- coding: utf-8 -*-
"""
@File    : challenge_type.py
@Date    : 2023-07-27
"""
from acme.challenges import HTTP01Response


class ChallengeType:
    # HTTP01Response.typ
    HTTP01 = 'http-01'

    # DNS01Response.typ
    DNS01 = 'dns-01'

    # TLSALPN01Response.typ
    TLSALPN01 = 'tls-alpn-01'
