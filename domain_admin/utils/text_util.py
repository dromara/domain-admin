# -*- coding: utf-8 -*-
"""
@File    : text_util.py
@Date    : 2023-05-30
"""
import re


def has_chinese(text: str) -> bool:
    """
    判断是否包含中文
    :param text:
    :return:
    """
    result = re.match("[\u4e00-\u9fa5]+", text)
    return True if result else False


def extract_chinese(text: str) -> str:
    """
    提取包含的中文
    :param text:
    :return:
    """
    result = re.match("[\u4e00-\u9fa5]+", text)
    if result:
        return result.group(0)
    else:
        return ""
