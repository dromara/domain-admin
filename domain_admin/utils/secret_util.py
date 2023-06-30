# -*- coding: utf-8 -*-
"""
secret_util.py
"""
import secrets


def get_random_secret():
    return secrets.token_hex()
