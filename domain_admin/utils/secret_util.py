# -*- coding: utf-8 -*-
import secrets


def get_random_secret():
    return secrets.token_hex()
