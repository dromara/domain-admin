# -*- coding: utf-8 -*-
"""
@File    : validate_util.py
@Date    : 2023-11-11
"""
import re


def is_phone(phone):
    """
    判断是否为手机号
    :param phone: str/none
    :return: bool
    """
    if not phone:
        return False

    result = re.match('^1[34578]\d{9}$', phone)
    return True if result else False


def is_email(email):
    """
    判断是否为邮箱
    :param email: str/none
    :return: bool
    """
    if not email:
        return False

    result = re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email)

    return True if result else False


def is_domain(domain):
    """
    判断是否为域名
    https://www.cnblogs.com/panpanwelcome/p/7464511.html
    :param domain: str/none
    :return: bool
    """
    if not domain:
        return False

    result = re.match('^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$', domain)

    return True if result else False

