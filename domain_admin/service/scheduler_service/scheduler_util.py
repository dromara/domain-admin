# -*- coding: utf-8 -*-
"""
@File    : scheduler_util.py
@Date    : 2024-01-28
@Author  : Peng Shiyu
"""


def crontab_compatible_weekday(expr):
    """
    :param expr:
    :return:

    bugfix: 0-6表示周一到周日，改为周日到周六，并支持7为周日
    day_of_week: number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    ref: https://github.com/agronholm/apscheduler/issues/286#issuecomment-449273964
    """
    if expr == "*":
        return expr

    mapping = {
        "0": "sun",
        "1": "mon",
        "2": "tue",
        "3": "wed",
        "4": "thu",
        "5": "fri",
        "6": "sat",
        "7": "sun"
    }

    return "".join(map(lambda x: mapping.get(x, x), expr))
