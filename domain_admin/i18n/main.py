# -*- coding: utf-8 -*-
"""
@File    : main.py
@Date    : 2023-08-04
"""
from flask import request

from domain_admin.config import LANGUAGE_KEY
from domain_admin.i18n.config import translate_config

translate_map = {}

for item in translate_config:
    translate_map[item['zh-CN']] = item


def translate(text):
    language = 'zh-CN'

    try:
        language = request.headers.get(LANGUAGE_KEY)
    except Exception as e:
        pass

    if text in translate_map:
        return translate_map[text].get(language) or text
    else:
        return text
